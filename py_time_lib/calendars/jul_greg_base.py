class JulGregBaseDate:
  'Base class for Julian and Gregorian calendars. This class not intended to be directly instantiated.'
  
  # static stuff
  
  MONTHS_IN_YEAR = 12
  MONTH_DAYS_NON_LEAP = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  
  @classmethod
  def days_in_year(cls, year):
    return 366 if cls.is_leap(year) else 365
  
  @classmethod
  def days_in_month(cls, year, month):
    if not (1 <= month <= cls.MONTHS_IN_YEAR):
      raise Exception(f'month {month} out of range, must be between 1 and {cls.MONTHS_IN_YEAR}')
    
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
  def normalize_date(cls, year, month, day):
    return cls.days_since_epoch_to_date(*cls.date_to_days_since_epoch(year, month, day))
  
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
  
  # instance stuff
  
  __slots__ = '_year', '_month', '_day'
  
  def __init__(self, year, month, day):
    if not (1 <= month <= self.MONTHS_IN_YEAR):
      raise Exception(f'month {month} out of range, must be between 1 and {self.MONTHS_IN_YEAR}')
    
    if not (1 <= day <= self.days_in_month(year, month)):
      raise Exception(f'day {year}-{month}-{day} out of range, must be between 1 and {self.days_in_month(year, month)}')
    
    self._year = year
    self._month = month
    self._day = day
  
  @classmethod
  def from_unnormalized(cls, year, month, day):
    'Creates a JulianDate object but accepts months and days out of range'
    return cls(cls.normalize_date(year, month, day))
  
  @property
  def year(self):
    return self._year
  
  @property
  def month(self):
    return self._month
  
  @property
  def day(self):
    return self._day
  
  def __repr__(self):
    return f'{self.__class__.__name__}({self.year!r}, {self.month!r}, {self.day!r})'
  
  def __str__(self):
    return f'{self.year}-{self.month:0>2}-{self.day:0>2}'
