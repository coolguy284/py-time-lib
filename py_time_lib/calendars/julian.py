from .jul_greg_base import JulGregBaseDate

class JulianDate(JulGregBaseDate):
  # static stuff
  
  REPEAT_PERIOD_DAYS = 366 + 365 * 3
  REPEAT_PERIOD_YEARS = 4
  
  @staticmethod
  def is_leap(year):
    return year % 4 == 0

JulianDate._init_class_vars()
