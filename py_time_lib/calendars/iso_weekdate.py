from numbers import Integral
from typing import Self

from .date_base import DateBase
from .gregorian import GregorianDate

class IsoWeekDate(DateBase):
  # static stuff
  
  DAYS_IN_WEEK = 7
  
  @staticmethod
  def weeks_in_year(year: Integral) -> int:
    ...
  
  @classmethod
  def date_to_days_since_epoch[T: Integral](cls, year: T, week: T, day: T) -> T:
    ...
  
  @classmethod
  def days_since_epoch_to_date[T: Integral](cls, days_since_epoch: T) -> tuple[T, T, T]:
    ...
  
  @classmethod
  def parse_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-WXX-DD" or "-YYYY-WXX-DD" to date tuple.'
    ...
  
  # instance stuff
  
  __slots__ = '_year', '_week', '_day'
  _year: Integral
  _week: Integral
  _day: Integral
  
  def __init__(self, *args: tuple['str | Integral | DateBase'] | tuple[Integral, Integral, Integral]):
    if len(args) == 0:
      raise Exception(f'{self.__class__.__name__} constructor needs an argument')
    elif len(args) == 1:
      if isinstance(args[0], str):
        iso_string = args[0]
        year, week, day = self.parse_iso_string(iso_string)
        days_since_epoch = self.date_to_days_since_epoch(year, week, day)
        self._days_since_epoch = days_since_epoch
        self._year = year
        self._week = week
        self._day = day
      elif isinstance(args[0], Integral):
        days_since_epoch = args[0]
        self._days_since_epoch = days_since_epoch
        self._year, self._week, self._day = self.days_since_epoch_to_date(days_since_epoch)
      elif isinstance(args[0], DateBase):
        date = args[0]
        self._days_since_epoch = date.days_since_epoch
        self._year, self._week, self._day = self.days_since_epoch_to_date(self._days_since_epoch)
      else:
        raise Exception(f'Unrecognized single argument {args[0]!r}')
    elif len(args) == 3:
      year, week, day = args
      
      weeks_in_year = self.weeks_in_year(year)
      
      if not (1 <= week <= weeks_in_year):
        raise Exception(f'week {year}-W{week} out of range, must be between 1 and {weeks_in_year}')
      
      if not (1 <= day <= self.DAYS_IN_WEEK):
        raise Exception(f'day {day} out of range, must be between 1 and {self.DAYS_IN_WEEK}')
      
      self._days_since_epoch = self.date_to_days_since_epoch(year, week, day)
      self._year = year
      self._week = week
      self._day = day
    else:
      raise Exception(f'{self.__class__.__name__} constructor takes 1 or 3 arguments')
  
  @classmethod
  def from_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-WXX-DD" or "-YYYY-WXX-DD" to date object.'
    ...
  
  @property
  def year(self) -> Integral:
    return self._year
  
  @property
  def week(self) -> Integral:
    return self._week
  
  @property
  def day(self) -> Integral:
    return self._day
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}(year = {self.year!r}, week = {self.week!r}, day = {self.day!r})'
  
  def __str__(self) -> str:
    return self.to_iso_string()
  
  def to_date_tuple(self) -> tuple[Integral, Integral, Integral]:
    ...
  
  def to_iso_string(self) -> str:
    ...
