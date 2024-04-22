from .jul_greg_base import JulGregBaseDate

class JulianDate(JulGregBaseDate):
  # static stuff
  
  JAN_1_YEAR0_DAY_OFFSET = -2
  REPEAT_PERIOD_DAYS = JulGregBaseDate.DAYS_LEAP_YEAR + JulGregBaseDate.DAYS_NON_LEAP_YEAR * 3
  REPEAT_PERIOD_YEARS = 4
  
  @staticmethod
  def is_leap(year) -> bool:
    return year % 4 == 0
  
  # instance stuff
  
  __slots__ = ()

JulianDate._init_class_vars()
