import re
from abc import abstractmethod, ABC
from numbers import Integral
from typing import Self

from ..lib_funcs import binary_search

class JulGregBaseDate(ABC):
  'Base class for Julian and Gregorian calendars. This class not intended to be directly instantiated.'
  
  # static stuff
  
  MONTHS_IN_YEAR = 12
  MONTH_DAYS_NON_LEAP = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  DAY_OF_WEEK_OFFSET = -1
  DAYS_IN_WEEK = 7
  _date_iso_string_regex = re.compile('^(-?\\d+)-(\\d{1,2})-(\\d{1,2})$')
  
  @staticmethod
  @abstractmethod
  def is_leap(year: Integral) -> bool:
    ...
  
  @classmethod
  def days_in_year(cls, year: Integral) -> int:
    return 366 if cls.is_leap(year) else 365
  
  @classmethod
  def days_in_month(cls, year: Integral, month: Integral) -> int:
    if not (1 <= month <= cls.MONTHS_IN_YEAR):
      raise Exception(f'month {month} out of range, must be between 1 and {cls.MONTHS_IN_YEAR}')
    
    if cls.is_leap(year):
      return cls.MONTH_DAYS_LEAP[month - 1]
    else:
      return cls.MONTH_DAYS_NON_LEAP[month - 1]
  
  @classmethod
  def normalize_date[T: Integral](cls, year: T, month: T, day: T) -> tuple[T, T, T]:
    return cls.days_since_epoch_to_date(cls.date_to_days_since_epoch(year, month, day))
  
  @classmethod
  def date_to_days_since_epoch[T: Integral](cls, year: T, month: T, day: T) -> T:
    year_addl, month = divmod(month - 1, cls.MONTHS_IN_YEAR)
    year += year_addl
    month += 1
    
    repeat_days = year // cls.REPEAT_PERIOD_YEARS * cls.REPEAT_PERIOD_DAYS
    mod_years = year % cls.REPEAT_PERIOD_YEARS
    mod_days = cls.months_start_day[mod_years * cls.MONTHS_IN_YEAR + (month - 1)]
    
    return repeat_days + mod_days + (day - 1) + cls.JAN_1_YEAR0_DAY_OFFSET
  
  @classmethod
  def days_since_epoch_to_date[T: Integral](cls, days: T) -> tuple[T, T, T]:
    days -= cls.JAN_1_YEAR0_DAY_OFFSET
    
    repeat_years = days // cls.REPEAT_PERIOD_DAYS * cls.REPEAT_PERIOD_YEARS
    mod_days = days % cls.REPEAT_PERIOD_DAYS
    representative_month_index = binary_search(lambda guess: cls.months_start_day[guess] <= mod_days, 0, len(cls.months_start_day))
    
    return (
      repeat_years + representative_month_index // cls.MONTHS_IN_YEAR,
      representative_month_index % cls.MONTHS_IN_YEAR + 1,
      mod_days - cls.months_start_day[representative_month_index] + 1
    )
  
  @classmethod
  def parse_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-MM-DD" or "-YYYY-MM-DD" to date tuple.'
    match = cls._date_iso_string_regex.match(string)
    return int(match[1]), int(match[2]), int(match[3])
  
  @classmethod
  def _init_class_vars(cls) -> None:
    cls.months_start_day = [0]
    
    for i in range(cls.REPEAT_PERIOD_YEARS * cls.MONTHS_IN_YEAR - 1):
      cls.months_start_day.append(cls.months_start_day[-1] + cls.days_in_month(i // cls.MONTHS_IN_YEAR, i % cls.MONTHS_IN_YEAR + 1))
    
    cls.DAYS_IN_YEAR = cls.REPEAT_PERIOD_DAYS / cls.REPEAT_PERIOD_YEARS
  
  # instance stuff
  
  __slots__ = '_days_since_epoch', '_year', '_month', '_day'
  _days_since_epoch: Integral
  _year: Integral
  _month: Integral
  _day: Integral
  
  # https://stackoverflow.com/questions/72644693/new-union-shorthand-giving-unsupported-operand-types-for-str-and-type/72644857#72644857
  def __init__(self, *args: tuple['str | Integral | JulGregBaseDate'] | tuple[Integral, Integral, Integral]):
    if len(args) == 0:
      raise Exception(f'JulGregBaseDate constructor needs an argument')
    elif len(args) == 1:
      if isinstance(args[0], str):
        iso_string = args[0]
        year, month, day = self.parse_iso_string(iso_string)
        days_since_epoch = self.date_to_days_since_epoch(year, month, day)
        self._days_since_epoch = days_since_epoch
        self._year = year
        self._month = month
        self._day = day
      elif isinstance(args[0], Integral):
        days_since_epoch = args[0]
        self._days_since_epoch = days_since_epoch
        self._year, self._month, self._day = self.days_since_epoch_to_date(days_since_epoch)
      elif isinstance(args[0], JulGregBaseDate):
        date = args[0]
        self._days_since_epoch = date.days_since_epoch
        self._year, self._month, self._day = self.days_since_epoch_to_date(self._days_since_epoch)
      else:
        raise Exception(f'Unrecognized single argument {args[0]!r}')
    elif len(args) == 3:
      year, month, day = args
      
      if not (1 <= month <= self.MONTHS_IN_YEAR):
        raise Exception(f'month {month} out of range, must be between 1 and {self.MONTHS_IN_YEAR}')
      
      if not (1 <= day <= self.days_in_month(year, month)):
        raise Exception(f'day {year}-{month}-{day} out of range, must be between 1 and {self.days_in_month(year, month)}')
      
      self._days_since_epoch = self.date_to_days_since_epoch(year, month, day)
      self._year = year
      self._month = month
      self._day = day
    else:
      raise Exception(f'JulGregBaseDate constructor takes 1 or 3 arguments')
  
  @classmethod
  def from_unnormalized(cls, year: Integral, month: Integral, day: Integral) -> Self:
    'Creates a JulianDate object but accepts months and days out of range'
    return cls(*cls.normalize_date(year, month, day))
  
  @classmethod
  def from_days_since_epoch(cls, days: Integral) -> Self:
    return cls(*cls.days_since_epoch_to_date(days))
  
  @classmethod
  def from_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-MM-DD" or "-YYYY-MM-DD" to date object.'
    return cls(*cls.parse_iso_string(string))
  
  @classmethod
  def from_ordinal_date(cls, year: Integral, ordinal_date: Integral):
    return cls.from_unnormalized(year, 1, ordinal_date)
  
  @property
  def days_since_epoch(self) -> Integral:
    return self._days_since_epoch
  
  @property
  def year(self) -> Integral:
    return self._year
  
  @property
  def month(self) -> Integral:
    return self._month
  
  @property
  def day(self) -> Integral:
    return self._day
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self.year!r}, {self.month!r}, {self.day!r})'
  
  def __str__(self) -> str:
    return self.to_iso_string()
  
  def to_date_tuple(self) -> tuple[Integral, Integral, Integral]:
    return (self.year, self.month, self.day)
  
  def to_days_since_epoch(self) -> Integral:
    return self._days_since_epoch
  
  def to_iso_string(self) -> str:
    return f'{self.year}-{self.month:0>2}-{self.day:0>2}'
  
  def ordinal_date(self) -> int:
    return self.days_since_epoch - self.__class__(self.year, 1, 1).days_since_epoch + 1
  
  def day_of_week(self) -> int:
    'Returns the day of week. 0 = sunday, 6 = saturday.'
    return (self.days_since_epoch + self.DAY_OF_WEEK_OFFSET) % self.DAYS_IN_WEEK
  
  def iso_day_of_week(self) -> int:
    'Returns the ISO day of week. 1 = monday, 7 = sunday.'
    return (self.day_of_week() - 1) % self.DAYS_IN_WEEK + 1
  
  def add_days(self, days: Integral) -> Self:
    return self.from_days_since_epoch(self.days_since_epoch + days)
