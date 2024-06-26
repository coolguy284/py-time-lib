from abc import abstractmethod
from datetime import date as datetime_date_cls
from math import ceil, floor
from numbers import Integral
from re import compile as re_compile
from typing import Self

from ..lib_funcs import binary_search
from ..named_tuples import MonthWeekDate
from .date_delta import DateDelta
from .date_base import DateBase
from .date_base_extras import ThreeTupleBase

class JulGregBaseDate(ThreeTupleBase):
  'Base class for Julian and Gregorian calendars. This class not intended to be directly instantiated.'
  
  # static stuff
  
  MONTHS_IN_YEAR = 12
  MONTH_DAYS_NON_LEAP = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  MONTH_DAYS_LEAP = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  DAYS_NON_LEAP_YEAR = sum(MONTH_DAYS_NON_LEAP)
  DAYS_LEAP_YEAR = sum(MONTH_DAYS_LEAP)
  MONTH_NAMES_LONG = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December',
  ]
  MONTH_NAMES_SHORT = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
  ]
  _date_iso_string_regex = re_compile(r'^(-?\d+)-(\d{1,2})-(\d{1,2})$')
  _calendar_month_row_inside_len = 22
  _empty_calendar_month_row = f'|{' ' * _calendar_month_row_inside_len}|'
  
  @staticmethod
  @abstractmethod
  def is_leap(year: Integral) -> bool:
    ...
  
  @classmethod
  def days_in_year(cls, year: Integral) -> int:
    return cls.DAYS_LEAP_YEAR if cls.is_leap(year) else cls.DAYS_NON_LEAP_YEAR
  
  @classmethod
  def days_in_month(cls, year: Integral, month: Integral) -> int:
    if not (1 <= month <= cls.MONTHS_IN_YEAR):
      raise ValueError(f'month {month} out of range, must be between 1 and {cls.MONTHS_IN_YEAR}')
    
    if cls.is_leap(year):
      return cls.MONTH_DAYS_LEAP[month - 1]
    else:
      return cls.MONTH_DAYS_NON_LEAP[month - 1]
  
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
  def days_since_epoch_to_date[T: Integral](cls, days_since_epoch: T) -> tuple[T, T, T]:
    days_since_epoch -= cls.JAN_1_YEAR0_DAY_OFFSET
    
    repeat_years = days_since_epoch // cls.REPEAT_PERIOD_DAYS * cls.REPEAT_PERIOD_YEARS
    mod_days = days_since_epoch % cls.REPEAT_PERIOD_DAYS
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
  def num_weeks_on_day(cls, year: Integral, month: Integral, day_of_week: Integral) -> Integral:
    'Returns the number of copies of a certain day of the week that are contained within the month.'
    first_week_of_month = cls.from_month_week_day(year, month, 1, day_of_week)
    next_month = cls.from_unnormalized(year, month + 1, 1)
    first_week_of_next_month = cls.from_month_week_day(next_month.year, next_month.month, 1, day_of_week)
    return (first_week_of_next_month.days_since_epoch - first_week_of_month.days_since_epoch) // cls.DAYS_IN_WEEK
  
  @classmethod
  def _init_class_vars(cls) -> None:
    cls.months_start_day = [0]
    
    for i in range(cls.REPEAT_PERIOD_YEARS * cls.MONTHS_IN_YEAR - 1):
      cls.months_start_day.append(cls.months_start_day[-1] + cls.days_in_month(i // cls.MONTHS_IN_YEAR, i % cls.MONTHS_IN_YEAR + 1))
    
    cls.DAYS_IN_YEAR = cls.REPEAT_PERIOD_DAYS / cls.REPEAT_PERIOD_YEARS
  
  # instance stuff
  
  __slots__ = '_month', '_day'
  _month: Integral
  _day: Integral
  
  # https://stackoverflow.com/questions/72644693/new-union-shorthand-giving-unsupported-operand-types-for-str-and-type/72644857#72644857
  def __init__[T: Integral | None](
      self,
      *args: tuple['str | Integral | DateBase | datetime_date_cls'] | tuple[Integral, Integral, Integral] | tuple[()],
      year: T = None, month: T = None, day: T = None
    ):
    if len(args) == 0:
      date_obj = self.__class__(year, month, day)
      
      self._days_since_epoch = date_obj.days_since_epoch
      self._year = date_obj.year
      self._month = date_obj.month
      self._day = date_obj.day
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
      elif isinstance(args[0], DateBase):
        date = args[0]
        self._days_since_epoch = date.days_since_epoch
        self._year, self._month, self._day = self.days_since_epoch_to_date(self._days_since_epoch)
      elif isinstance(args[0], datetime_date_cls):
        datetime_date = args[0]
        self._days_since_epoch = self.__class__.from_datetime_date(datetime_date)._days_since_epoch
        self._year, self._month, self._day = self.days_since_epoch_to_date(self._days_since_epoch)
      else:
        raise TypeError(f'Unrecognized single argument {args[0]!r}')
    elif len(args) == 3:
      year, month, day = args
      
      if not (1 <= month <= self.MONTHS_IN_YEAR):
        raise ValueError(f'month {month} out of range, must be between 1 and {self.MONTHS_IN_YEAR}')
      
      if not (1 <= day <= self.days_in_month(year, month)):
        raise ValueError(f'day {year}-{month}-{day} out of range, must be between 1 and {self.days_in_month(year, month)}')
      
      self._days_since_epoch = self.date_to_days_since_epoch(year, month, day)
      self._year = year
      self._month = month
      self._day = day
    else:
      raise TypeError(f'{self.__class__.__name__} constructor takes 1 or 3 arguments ({len(args)} given)')
  
  @classmethod
  def from_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-MM-DD" or "-YYYY-MM-DD" to date object.'
    return cls(*cls.parse_iso_string(string))
  
  @classmethod
  def from_ordinal_date(cls, year: Integral, ordinal_date: Integral) -> Self:
    return cls.from_unnormalized(year, 1, ordinal_date)
  
  @classmethod
  def from_month_week_day(cls, year: Integral, month: Integral, week: Integral, day_of_week: Integral, from_month_end: bool = False) -> Self:
    if not from_month_end:
      first_day_of_week = cls(year, month, 1).day_of_week()
      if day_of_week >= first_day_of_week:
        return cls(year, month, (week - 1) * cls.DAYS_IN_WEEK + (day_of_week - first_day_of_week) + 1)
      else:
        return cls(year, month, week * cls.DAYS_IN_WEEK + (day_of_week - first_day_of_week) + 1)
    else:
      week_flipped = cls.num_weeks_on_day(year, month, day_of_week) - week + 1
      return cls.from_month_week_day(year, month, week_flipped, day_of_week)
  
  @classmethod
  def from_month_day_of_week_comp_day(cls, year: Integral, month: Integral, day: Integral, day_of_week: Integral, greater_than_equals: bool, out_of_month_bounds_allowed: bool = True) -> Self:
    '''
    Returns a date in the month that is on the given day of week and
    greater than or equal to (or less than or equal to if greater_than_equals
    is False) the given date. For example, the first sunday in april 2024 that
    is less than or equal to the 25th of the month is apr 21.
    '''
    
    base_date = cls(year, month, day)
    base_day_of_week = base_date.day_of_week()
    
    if greater_than_equals:
      day_increment = (day_of_week - base_day_of_week) % cls.DAYS_IN_WEEK
      result = base_date + DateDelta(day_increment)
    else:
      day_decrement = (base_day_of_week - day_of_week) % cls.DAYS_IN_WEEK
      result = base_date - DateDelta(day_decrement)
    
    if not out_of_month_bounds_allowed:
      if result.month != base_date.month or result.year != base_date.year:
        raise ValueError('Calculating date of given day of week goes outside of month bounds')
    
    return result
  
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
    return f'{self.__class__.__name__}(year = {self.year!r}, month = {self.month!r}, day = {self.day!r})'
  
  def __str__(self) -> str:
    return self.to_iso_string()
  
  def to_date_tuple[T: Integral](self) -> tuple[T, T, T]:
    return (self.year, self.month, self.day)
  
  def to_iso_string(self) -> str:
    return f'{self.year}-{self.month:0>2}-{self.day:0>2}'
  
  def to_month_week_day(self, from_month_end: bool = False) -> MonthWeekDate:
    '''
    Returns a tuple of the form (year, month, week, day_of_week); for example "the second monday in january 2024"
    would result in (2024, 1, 2, 1). Weeks are numbered 0-6.
    '''
    
    if not from_month_end:
      # 1 = first 7 days of month, 2 = second 7 days of month, etc.
      week_num = (self.day - 1) // self.DAYS_IN_WEEK + 1

      return MonthWeekDate(self.year, self.month, week_num, self.day_of_week())
    else:
      year, month, week_num, day_of_week = self.to_month_week_day()
      
      week_num = self.num_weeks_on_day(self.year, self.month, day_of_week) - week_num + 1
      
      return MonthWeekDate(year, month, week_num, day_of_week)
  
  def get_monthly_calendar(self) -> str:
    header = f'{self.MONTH_NAMES_SHORT[self.month - 1]} {self.year}'
    header_half_blank_space = (self._calendar_month_row_inside_len - len(header)) / 2
    if header_half_blank_space > 0:
      header_low_half_blank_space = floor(header_half_blank_space)
      header_high_half_blank_space = ceil(header_half_blank_space)
      result = f'|{' ' * header_low_half_blank_space}{header}{' ' * header_high_half_blank_space}|\n'
    else:
      result = f'|{header}|\n'
    result += '------------------------\n'
    result += '| Su Mo Tu We Th Fr Sa |\n'
    start_of_month = self.__class__(self.year, self.month, 1)
    starting_index = start_of_month.day_of_week()
    num_days = self.days_in_month(self.year, self.month)
    past_week_row = None
    
    for i in range(num_days):
      week_row, current_week_index = divmod(i + starting_index, self.DAYS_IN_WEEK)
      if past_week_row == None:
        result += '| ' + '   ' * starting_index
      elif week_row > past_week_row:
        result += '|\n| '
      result += f'{i + 1:>2} '
      past_week_row = week_row
    
    result += '   ' * (self.DAYS_IN_WEEK - current_week_index - 1) + '|'
    
    return result
  
  def get_yearly_calendar(self, num_cols: Integral = 3, horizontal_padding: Integral = 1, vertical_padding: Integral = 1) -> str:
    result = ''
    
    working_rows = []
    past_row = None
    
    for month_index in range(self.MONTHS_IN_YEAR):
      row, col = divmod(month_index, num_cols)
      
      new_month_rows = self.__class__(self.year, month_index + 1, 1).get_monthly_calendar().split('\n')
      
      if past_row != row and past_row != None:
        if past_row != 0:
          result += '\n' + '\n' * vertical_padding
        result += '\n'.join((
          row_text + self._empty_calendar_month_row * (
            (
              (len(self._empty_calendar_month_row) + horizontal_padding) * num_cols - horizontal_padding - len(row_text)
            ) // len(self._empty_calendar_month_row)
          )
          for row_text in working_rows
        ))
        working_rows.clear()
      
      for month_line_index in range(len(new_month_rows)):
        if month_line_index < len(working_rows):
          working_rows[month_line_index] += (' ' * horizontal_padding) + new_month_rows[month_line_index]
        else:
          if col != 0:
            working_rows.append((self._empty_calendar_month_row + (' ' * horizontal_padding)) * col + new_month_rows[month_line_index])
          else:
            working_rows.append(new_month_rows[month_line_index])
      
      past_row = row
    
    if past_row != 0:
      result += '\n' + '\n' * vertical_padding
    num_cols_last_row = max((
      (len(row_text) + horizontal_padding) // (len(self._empty_calendar_month_row) + horizontal_padding)
      for row_text in working_rows
    ))
    result += '\n'.join((
      row_text + self._empty_calendar_month_row * (
        (
          (len(self._empty_calendar_month_row) + horizontal_padding) * num_cols_last_row - horizontal_padding - len(row_text)
        ) // len(self._empty_calendar_month_row)
      )
      for row_text in working_rows
    ))
    
    return result
