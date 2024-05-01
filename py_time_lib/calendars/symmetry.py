from numbers import Integral

from .jul_greg_base import JulGregBaseDate

# http://individual.utoronto.ca/kalendis/classic.htm
# http://individual.utoronto.ca/kalendis/symmetry.htm

class SymmetryBase(JulGregBaseDate):
  # static stuff
  
  MONTH_DAYS_NON_LEAP = [...]
  MONTH_DAYS_LEAP = [...]
  DAYS_NON_LEAP_YEAR = 364
  DAYS_LEAP_YEAR = 371
  JAN_1_YEAR0_DAY_OFFSET = 2
  REPEAT_PERIOD_YEARS = 293
  REPEAT_PERIOD_DAYS = 52 * DAYS_LEAP_YEAR + (REPEAT_PERIOD_YEARS - 52) * DAYS_NON_LEAP_YEAR
  
  def is_leap(year: Integral) -> bool:
    return (52 * year + 146) % 293 < 52
  
  # instance stuff
  
  __slots__ = ()

IRV_MONTH_NAMES_LONG = [
  'January', 'February', 'March', 'April',
  'May', 'June', 'July', 'August',
  'September', 'October', 'November', 'December',
  'Irvember',
]
IRV_MONTH_NAMES_SHORT = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Irv',
]

class Symmetry010(SymmetryBase):
  # static stuff
  
  MONTH_DAYS_NON_LEAP = [30, 31, 30, 30, 31, 30, 30, 31, 30, 30, 31, 30]
  MONTH_DAYS_LEAP = [30, 31, 30, 30, 31, 30, 30, 31, 30, 30, 31, 37]
  #DAYS_NON_LEAP_YEAR = sum(MONTH_DAYS_NON_LEAP)
  #DAYS_LEAP_YEAR = sum(MONTH_DAYS_LEAP)
  
  # instance stuff
  
  __slots__ = ()

Symmetry010._init_class_vars()

class Symmetry010LeapMonth(SymmetryBase):
  # static stuff
  
  MONTHS_IN_YEAR = 13
  MONTH_DAYS_NON_LEAP = [30, 31, 30, 30, 31, 30, 30, 31, 30, 30, 31, 30, 0]
  MONTH_DAYS_LEAP = [30, 31, 30, 30, 31, 30, 30, 31, 30, 30, 31, 30, 7]
  #DAYS_NON_LEAP_YEAR = sum(MONTH_DAYS_NON_LEAP)
  #DAYS_LEAP_YEAR = sum(MONTH_DAYS_LEAP)
  MONTH_NAMES_LONG = IRV_MONTH_NAMES_LONG
  MONTH_NAMES_SHORT = IRV_MONTH_NAMES_SHORT
  
  # instance stuff
  
  __slots__ = ()

Symmetry010LeapMonth._init_class_vars()

class Symmetry454(SymmetryBase):
  # static stuff
  
  MONTH_DAYS_NON_LEAP = [28, 35, 28, 28, 35, 28, 28, 35, 28, 28, 35, 28]
  MONTH_DAYS_LEAP = [28, 35, 28, 28, 35, 28, 28, 35, 28, 28, 35, 35]
  #DAYS_NON_LEAP_YEAR = sum(MONTH_DAYS_NON_LEAP)
  #DAYS_LEAP_YEAR = sum(MONTH_DAYS_LEAP)
  
  # instance stuff
  
  __slots__ = ()

Symmetry454._init_class_vars()

class Symmetry454LeapMonth(SymmetryBase):
  # static stuff
  
  MONTHS_IN_YEAR = 13
  MONTH_DAYS_NON_LEAP = [28, 35, 28, 28, 35, 28, 28, 35, 28, 28, 35, 28, 0]
  MONTH_DAYS_LEAP = [28, 35, 28, 28, 35, 28, 28, 35, 28, 28, 35, 28, 7]
  #DAYS_NON_LEAP_YEAR = sum(MONTH_DAYS_NON_LEAP)
  #DAYS_LEAP_YEAR = sum(MONTH_DAYS_LEAP)
  MONTH_NAMES_LONG = IRV_MONTH_NAMES_LONG
  MONTH_NAMES_SHORT = IRV_MONTH_NAMES_SHORT
  
  # instance stuff
  
  __slots__ = ()

Symmetry454LeapMonth._init_class_vars()
