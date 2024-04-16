import unittest

from py_time_lib import TimeInstant

from py_time_lib.tests.test_calendar_gregorian import TestCalendarGregorian
from py_time_lib.tests.test_calendar_holocene import TestCalendarHolocene
from py_time_lib.tests.test_calendar_isoweek import TestCalendarIsoWeek
from py_time_lib.tests.test_calendar_julian import TestCalendarJulian
from py_time_lib.tests.test_fixed_prec import TestFixedPrec
from py_time_lib.tests.test_lib_funcs import TestLibFuncs
from py_time_lib.tests.test_time_classes import TestTimeClasses

TimeInstant.update_leap_seconds()
unittest.main()
