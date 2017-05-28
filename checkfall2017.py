#! /usr/local/bin/python
from course_checker import *

# Frequency
freq = 15 * 60

# Initialize
checker = CourseChecker()
checker.setFreq(freq)

# Year, Term, Subject, Number, CRN
checker.add_course(2017, "Fall", "CS", 425, 57769)

# Start
checker.check()
