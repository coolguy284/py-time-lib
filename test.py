import unittest

from py_time_lib import update_time_databases

from py_time_lib.tests.calendars.test_calendar_gregorian import TestCalendarGregorian
from py_time_lib.tests.calendars.test_calendar_holocene import TestCalendarHolocene
from py_time_lib.tests.calendars.test_calendar_isoweek import TestCalendarIsoWeek
from py_time_lib.tests.calendars.test_calendar_julian import TestCalendarJulian
from py_time_lib.tests.calendars.test_calendar_date_base import TestCalendarDateBase
from py_time_lib.tests.time_classes.test_time_classes import TestTimeClasses
from py_time_lib.tests.test_fixed_prec import TestFixedPrec
from py_time_lib.tests.test_lib_funcs import TestLibFuncs

update_time_databases()

# fixes test error diff not being full length despite self.maxDiff = None
# https://stackoverflow.com/questions/43842675/how-to-prevent-truncating-of-string-in-unit-test-python/61345284#61345284
if 'unittest.util' in __import__('sys').modules:
  # Show full diff in self.assertEqual.
  __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

unittest.main()
#unittest.main(argv = ['test.py', '--durations=0'])
