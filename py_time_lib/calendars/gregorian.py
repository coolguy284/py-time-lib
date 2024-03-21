MONTH_DAYS_NON_LEAP = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
REPEAT_PERIOD_DAYS = ((366 + 365 * 3) * 24 + (365 * 4)) * 3 + (366 + 365 * 3) * 25
REPEAT_PERIOD_YEARS = 400

def is_leap(year):
  return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)

def days_in_year(year):
  return 366 if is_leap(year) else 365

def days_in_month(year, month):
  if not (1 <= month <= 12):
    raise Exception(f'month {month} out of range, must be between 1 and 12')
  
  if is_leap(year):
    return MONTH_DAYS_LEAP[month - 1]
  else:
    return MONTH_DAYS_NON_LEAP[month - 1]

class GregorianDate:
  __slots__ = '_year', '_month', '_day'
  
  def __init__(self, year, month, day):
    if not (1 <= month <= 12):
      raise Exception(f'month {month} out of range, must be between 1 and 12')
    
    if not (1 <= day <= days_in_month(year, month)):
      raise Exception(f'day {year}-{month}-{day} out of range, must be between 1 and {days_in_month(year, month)}')
    
    self._year = year
    self._month = month
    self._day = day
  
  @classmethod
  def from_unnormalized(cls, year, month, day):
    'Creates a GregorianDate object but accepts months and days out of range'
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
