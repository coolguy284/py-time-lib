from numbers import Integral

from .jul_greg_base import JulGregBaseDate
from .julian import JulianDate

class GregorianDate(JulGregBaseDate):
  # static stuff
  
  JAN_1_YEAR0_DAY_OFFSET = 0
  REPEAT_PERIOD_DAYS = ((366 + 365 * 3) * 24 + (365 * 4)) * 3 + (366 + 365 * 3) * 25
  REPEAT_PERIOD_YEARS = 400
  
  @staticmethod
  def is_leap(year) -> bool:
    return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)
  
  # instance stuff
  
  __slots__ = ()
  
  def days_diff_from_julian(self) -> Integral:
    return JulianDate(*self.to_date()).to_days_since_epoch() - self.to_days_since_epoch()

GregorianDate._init_class_vars()
