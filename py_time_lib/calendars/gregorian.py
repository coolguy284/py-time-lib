from numbers import Integral

from .jul_greg_base import JulGregBaseDate
from .julian import JulianDate
from .iso_weekdate import IsoWeekDate

class GregorianDate(JulGregBaseDate):
  # static stuff
  
  JAN_1_YEAR0_DAY_OFFSET = 0
  REPEAT_PERIOD_DAYS = ((366 + 365 * 3) * 24 + (365 * 4)) * 3 + (366 + 365 * 3) * 25
  REPEAT_PERIOD_YEARS = 400
  
  @staticmethod
  def is_leap(year) -> bool:
    return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)
  
  @classmethod
  def from_iso_week_tuple(cls, year: Integral, week: Integral, day: Integral):
    return cls(IsoWeekDate(year, week, day))
  
  # instance stuff
  
  __slots__ = ()
  
  def days_diff_from_julian(self) -> Integral:
    '''
    Reports the difference in days between the julian and gregorian calendar.
    Positive numbers mean the gregorian date corresponding to today is ahead
    of the julian date.
    '''
    return JulianDate(*self.to_date_tuple()).days_since_epoch - self.days_since_epoch
  
  def to_iso_week_tuple(self) -> tuple[int, int, int]:
    'Converts the current date to a tuple of (year, week, day)'
    return IsoWeekDate(self).to_date_tuple()

GregorianDate._init_class_vars()
