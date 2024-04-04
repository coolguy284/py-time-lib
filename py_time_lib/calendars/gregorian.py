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
  
  @classmethod
  def num_weeks_in_iso_week_year(cls, year):
    day_of_week_dec_31 = cls(year, 12, 31).iso_day_of_week()
    day_of_week_dec_31_past_year = cls(year - 1, 12, 31).iso_day_of_week()
    if day_of_week_dec_31 == 4 or day_of_week_dec_31_past_year == 3:
      return 53
    else:
      return 52
  
  def to_iso_week_tuple(self) -> tuple[int, int, int]:
    'Converts the current date to a tuple of (year, week, day)'
    # https://en.wikipedia.org/wiki/ISO_week_date#Algorithms
    ordinal_date = self.ordinal_date()
    iso_day_of_week = self.iso_day_of_week()
    year = self.year
    week_number = (ordinal_date - iso_day_of_week + 10) // 7
    
    if week_number == 0:
      year -= 1
      week_number = self.num_weeks_in_iso_week_year(self.year - 1)
    elif week_number == 53:
      if self.num_weeks_in_iso_week_year(self.year) != 53:
        year += 1
        week_number = 1
    
    return year, week_number, iso_day_of_week

GregorianDate._init_class_vars()
