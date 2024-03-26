from .jul_greg_base import JulGregBaseDate

class GregorianDate(JulGregBaseDate):
  # static stuff
  
  REPEAT_PERIOD_DAYS = ((366 + 365 * 3) * 24 + (365 * 4)) * 3 + (366 + 365 * 3) * 25
  REPEAT_PERIOD_YEARS = 400
  
  @staticmethod
  def is_leap(year):
    return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)

GregorianDate._init_class_vars()
