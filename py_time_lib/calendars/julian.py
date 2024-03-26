MONTHS_IN_YEAR = 12
MONTH_DAYS_NON_LEAP = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
REPEAT_PERIOD_DAYS = 366 + 365 * 3
REPEAT_PERIOD_YEARS = 4

def is_leap(year):
  return year % 4 == 0

def days_in_year(year):
  return 366 if is_leap(year) else 365

def days_in_month(year, month):
  if not (1 <= month <= MONTHS_IN_YEAR):
    raise Exception(f'month {month} out of range, must be between 1 and {MONTHS_IN_YEAR}')
  
  if is_leap(year):
    return MONTH_DAYS_LEAP[month - 1]
  else:
    return MONTH_DAYS_NON_LEAP[month - 1]

months_start_day = [0]

for i in range(REPEAT_PERIOD_YEARS * MONTHS_IN_YEAR - 1):
  months_start_day.append(months_start_day[-1] + days_in_month(i // MONTHS_IN_YEAR, i % MONTHS_IN_YEAR + 1))

def date_to_days_since_epoch(year, month, day):
  year_addl, month = divmod(month, MONTHS_IN_YEAR)
  year += year_addl
  
  repeat_days = year // REPEAT_PERIOD_YEARS * REPEAT_PERIOD_DAYS
  mod_years = year % REPEAT_PERIOD_YEARS
  mod_days = months_start_day[mod_years * MONTHS_IN_YEAR + (month - 1)]
  return repeat_days + mod_days + (day - 1)

def days_since_epoch_to_date(days):
  repeat_years = days // REPEAT_PERIOD_DAYS * REPEAT_PERIOD_YEARS
  mod_days = days % REPEAT_PERIOD_DAYS
  low_enough_index = 0
  too_high_index = len(months_start_day)
  while too_high_index - low_enough_index > 1:
    guess_index = (low_enough_index + too_high_index) // 2
    if months_start_day[guess_index] > mod_days:
      # too high
      too_high_index = guess_index
    else:
      # could be valid
      low_enough_index = guess_index
  return (
    repeat_years + low_enough_index // MONTHS_IN_YEAR,
    low_enough_index % MONTHS_IN_YEAR + 1,
    mod_days - months_start_day[low_enough_index] + 1
  )

class JulianDate:
  __slots__ = '_year', '_month', '_day'
  
  def __init__(self, year, month, day):
    if not (1 <= month <= MONTHS_IN_YEAR):
      raise Exception(f'month {month} out of range, must be between 1 and {MONTHS_IN_YEAR}')
    
    if not (1 <= day <= days_in_month(year, month)):
      raise Exception(f'day {year}-{month}-{day} out of range, must be between 1 and {days_in_month(year, month)}')
    
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
