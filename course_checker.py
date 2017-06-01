# Coding Style Staff: Use .join() instead of +, .format() instead of %,
# while 1 instead of true, == != instead of is/is not
# Reformat from rebot.py, thanks to its author

# import requests as req
from lxml import etree as et
from pyquery import PyQuery as pq
from termcolor import colored
import webbrowser
import os
import time
import mechanize
import cookielib
import getpass
import csv

UNAVAILABLE = ["Closed", "UNKNOWN", "Pending"]
TITLE = "Course Checker"
SOUND = "default"
TERM = {"spring": 1, "summer": 5, "fall": 8, "winter": 0}
REGISTER = 'https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1&target=A'
class CourseChecker(object):
    def __init__(self):
        self.freq = None
        self.urls = []
        self.messages = []
        self.num = 0
        self.loggedin = False
        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()

        # Configure Browser
        self.br.set_cookiejar(self.cj)
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', 'Chrome')]

    # Start login process
    def login(self):
        netid = raw_input("NetID: ")
        password = getpass.getpass()

        self.br.open('https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1')
        self.br.select_form(nr=0)

        # User credentials
        self.br.form['inputEnterpriseId'] = netid
        self.br.form['password'] = password

        # Login
        self.br.submit()
        self.loggedin = True

    # Take in a message dictonary
    def notify(self, messages, available):
        t = "-title {!r}".format(TITLE)
        s = "-subtitle {!r}".format(messages["course"])
        m = "-message {!r}".format(messages["available"])
        if messages["sound"] is not None:
            sd = "-sound {!r}".format(messages["sound"])
            os.system("terminal-notifier {}".format(' '.join([m, t, s, sd])))
        else:
            os.system("terminal-notifier {}".format(' '.join([m, t, s])))

    def add_course(self, year, term, subject, number, crn):
        # Urls
        url = {}
        url["status"] = "http://courses.illinois.edu/cisapp/explorer/schedule/" + str(year) + '/' + term.lower() + '/' + subject.upper() + '/' + str(number) + '/' + str(crn) + '.xml'
        url["capacity"] = "https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=1" + str(year) + str(TERM[term.lower()]) + "&crn_in=" + str(crn)
        self.urls.append(url)

        # Messages
        message = {}
        message["course"] = subject.upper() + str(number)
        message["available"] = message["course"] + " is available"
        message["sound"] = SOUND
        self.messages.append(message)

        self.num += 1

    # Mainly helper method
    def add_course_from_list(self, course):
        year, term, subject, number, crn = course
        self.add_course(int(year), term, subject, int(number), int(crn))

    def add_course_from_csv(self, filename="./courses.csv", header=True):
        with open(filename, 'r') as f:
            courses = csv.reader(f.read().splitlines())
            if header:
                courses.next()

            for course in courses:
                self.add_course_from_list(course)

    def printCapacity(self, result):
        if result["cross"]:
            print(str(result["actual"][0]) + "/" + str(result["capacity"][0]) + "   " + "Rem: " + str(result["remaining"][0]))
            print(str(result["actual"][1]) + "/" + str(result["capacity"][1]) + "   " + "Rem: " + str(result["remaining"][1]))
            print('')
        else:
            print(str(result["actual"][0]) + "/" + str(result["capacity"][0]) + "   " + "Rem: " + str(result["remaining"][0]))
            print('')

    def printStatus(self, status, course):
            if status == "Closed":
                text = colored(course + ": " + status, "red")
            elif status == "UNKNOWN" or status == "Pending":
                text = colored(course + ": " + status, "yellow")
            else:
                text = colored(course + ": " + status, "green")
            print(text)

    def getCapacity(self, url):
        res = self.br.open(url)
        cls = pq(res.read())("table.datadisplaytable tr")

        result = {}
        # result["description"] = pq(cls[0]).text()
        try:
            result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),int(pq(pq(cls[5])("td")[0]).text())]
            result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),int(pq(pq(cls[5])("td")[1]).text())]
            result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),int(pq(pq(cls[5])("td")[2]).text())]
            result["cross"] = True
        except:
            result["capacity"]=[int(pq(pq(cls[3])("td")[0]).text()),1]
            result["actual"]=[int(pq(pq(cls[3])("td")[1]).text()),1]
            result["remaining"]=[int(pq(pq(cls[3])("td")[2]).text()),1]
            result["cross"] = False
        return result

    def getStatus(self, url):
        res = self.br.open(url)
        tree = et.fromstring(res.read())
        status = tree.xpath("//enrollmentStatus/text()")[0]
        return status

    def setFreq(self):
        try:
            self.freq = int(raw_input("Frequency: "))
        except:
            # Default to 10 min
            self.freq = 600

    def check(self):
        if not self.loggedin:
            self.login()

        if not self.freq:
            self.setFreq()

        print('')
        while 1:
            print("------------------------------------------")
            print("Attempt at " + time.ctime())
            print("------------------------------------------")

            # Only open one registration page when multiple course available
            opened = False
            for i in xrange(self.num):
                url = self.urls[i]
                message = self.messages[i]
                status = self.getStatus(url["status"])
                capacity_result = self.getCapacity(url["capacity"])
                self.printStatus(status, message["course"])
                self.printCapacity(capacity_result)

                if status not in UNAVAILABLE:
                    self.notify(message)
                    if not opened:
                        webbrowser.open_new(REGISTER)
                        opened = True



            # Default frequency to 10 min
            time.sleep(self.freq)
