import requests as req
from lxml import etree as et

year = raw_input("Year: ")
term = raw_input("Term: ")
subject = raw_input("Subject: ")
num = raw_input("Course Number: ")
crn = raw_input("Section CRN: ")
term = term.lower()
subject = subject.upper()
url = 'http://courses.illinois.edu/cisapp/explorer/schedule/' + year + '/' + term + '/' + subject + '/' + num + '/' + crn + '.xml'

r = req.get(url)
tree = et.fromstring(r.content)
stat = tree.xpath("//enrollmentStatus/text()")
print(stat[0])
