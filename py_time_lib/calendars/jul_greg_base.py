class JulGregBaseDate:
  'Base class for Julian and Gregorian calendars. This class not intended to be directly instantiated.'
  
  # static stuff
  
  MONTHS_IN_YEAR = 12
  MONTH_DAYS_NON_LEAP = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  
  # instance stuff
  
  __slots__ = '_year', '_month', '_day'
  
  def __init__(self, year, month, day):
    if not (1 <= month <= self.__class__.MONTHS_IN_YEAR):
      raise Exception(f'month {month} out of range, must be between 1 and {self.__class__.MONTHS_IN_YEAR}')
    
    if not (1 <= day <= self.__class__.days_in_month(year, month)):
      raise Exception(f'day {year}-{month}-{day} out of range, must be between 1 and {self.__class__.days_in_month(year, month)}')
    
    self._year = year
    self._month = month
    self._day = day
  
  @classmethod
  def from_unnormalized(cls, year, month, day):
    'Creates a JulianDate object but accepts months and days out of range'
    pass
  
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
