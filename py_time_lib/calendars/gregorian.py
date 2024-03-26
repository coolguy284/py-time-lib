from .jul_greg_base import JulGregBaseDate

class GregorianDate(JulGregBaseDate):
  # static stuff
  
  REPEAT_PERIOD_DAYS = ((366 + 365 * 3) * 24 + (365 * 4)) * 3 + (366 + 365 * 3) * 25
  REPEAT_PERIOD_YEARS = 400
  
  @staticmethod
  def is_leap(year):
    return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)
  
  @classmethod
  def days_in_year(cls, year):
    return 366 if cls.is_leap(year) else 365
  
  @classmethod
  def days_in_month(cls, year, month):
    if not (1 <= month <= 12):
      raise Exception(f'month {month} out of range, must be between 1 and 12')
    
    if cls.is_leap(year):
      return cls.MONTH_DAYS_LEAP[month - 1]
    else:
      return cls.MONTH_DAYS_NON_LEAP[month - 1]
  
  @classmethod
  def _get_months_start_day(cls):
    months_start_day = [0]
    
    for i in range(cls.REPEAT_PERIOD_YEARS * cls.MONTHS_IN_YEAR - 1):
      months_start_day.append(months_start_day[-1] + cls.days_in_month(i // cls.MONTHS_IN_YEAR, i % cls.MONTHS_IN_YEAR + 1))
    
    return months_start_day
  
  @classmethod
  def date_to_days_since_epoch(cls, year, month, day):
    year_addl, month = divmod(month - 1, cls.MONTHS_IN_YEAR)
    year += year_addl
    month += 1
    
    repeat_days = year // cls.REPEAT_PERIOD_YEARS * cls.REPEAT_PERIOD_DAYS
    mod_years = year % cls.REPEAT_PERIOD_YEARS
    mod_days = cls.months_start_day[mod_years * cls.MONTHS_IN_YEAR + (month - 1)]
    return repeat_days + mod_days + (day - 1)
  
  @classmethod
  def days_since_epoch_to_date(cls, days):
    repeat_years = days // cls.REPEAT_PERIOD_DAYS * cls.REPEAT_PERIOD_YEARS
    mod_days = days % cls.REPEAT_PERIOD_DAYS
    low_enough_index = 0
    too_high_index = len(cls.months_start_day)
    while too_high_index - low_enough_index > 1:
      guess_index = (low_enough_index + too_high_index) // 2
      if cls.months_start_day[guess_index] > mod_days:
        # too high
        too_high_index = guess_index
      else:
        # could be valid
        low_enough_index = guess_index
    return (
      repeat_years + low_enough_index // cls.MONTHS_IN_YEAR,
      low_enough_index % cls.MONTHS_IN_YEAR + 1,
      mod_days - cls.months_start_day[low_enough_index] + 1
    )

GregorianDate.months_start_day = GregorianDate._get_months_start_day()
