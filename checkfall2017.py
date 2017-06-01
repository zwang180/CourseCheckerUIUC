#! /usr/local/bin/python
from course_checker import *

# Initialize
checker = CourseChecker()
# checker.setFreq(freq)
# checker.login()

# Year, Term, Subject, Number, CRN
# checker.add_course(2017, "Fall", "CS", 425, 57769)
checker.add_course_from_csv()

# Start
checker.check()
