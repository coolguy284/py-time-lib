from numbers import Integral

from .jul_greg_base import JulGregBaseDate
from .julian import JulianDate
from .iso_weekdate import IsoWeekDate

class GregorianDate(JulGregBaseDate):
  # static stuff
  
  JAN_1_YEAR0_DAY_OFFSET = 0
  REPEAT_PERIOD_DAYS = ((JulGregBaseDate.DAYS_LEAP_YEAR + JulGregBaseDate.DAYS_NON_LEAP_YEAR * 3) * 24 + (JulGregBaseDate.DAYS_NON_LEAP_YEAR * 4)) * 3 + (JulGregBaseDate.DAYS_LEAP_YEAR + JulGregBaseDate.DAYS_NON_LEAP_YEAR * 3) * 25
  REPEAT_PERIOD_YEARS = 400
  
  @staticmethod
  def is_leap(year) -> bool:
    return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)
  
  # instance stuff
  
  __slots__ = ()
  
  def days_diff_from_julian(self) -> Integral:
    '''
    Reports the difference in days between the julian and gregorian calendar.
    Positive numbers mean the gregorian date corresponding to today is ahead
    of the julian date.
    '''
    return JulianDate(*self.to_date_tuple()).days_since_epoch - self.days_since_epoch

GregorianDate._init_class_vars()
