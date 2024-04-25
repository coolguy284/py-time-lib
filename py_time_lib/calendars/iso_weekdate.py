import re
from datetime import date as datetime_date_cls
from numbers import Integral
from typing import Self

from .date_base import DateBase
from . import gregorian

class IsoWeekDate(DateBase):
  # static stuff
  
  _date_iso_string_regex = re.compile(r'^(-?\d+)-W(\d{1,2})-(\d)$')
  
  @staticmethod
  def weeks_in_year(year: Integral) -> int:
    day_of_week_dec_31 = gregorian.GregorianDate(year, 12, 31).iso_day_of_week()
    day_of_week_dec_31_past_year = gregorian.GregorianDate(year - 1, 12, 31).iso_day_of_week()
    if day_of_week_dec_31 == 4 or day_of_week_dec_31_past_year == 3:
      return 53
    else:
      return 52
  
  @classmethod
  def date_to_days_since_epoch[T: Integral](cls, year: T, week: T, day: T) -> T:
    # https://en.wikipedia.org/wiki/ISO_week_date#Algorithms
    d = week * cls.DAYS_IN_WEEK + day - (gregorian.GregorianDate(year, 1, 4).iso_day_of_week() + 3)
    
    if d < 1:
      gregorian_year = year - 1
      ordinal_day = d + gregorian.GregorianDate.days_in_year(year - 1)
    elif d > gregorian.GregorianDate.days_in_year(year):
      gregorian_year = year + 1
      ordinal_day = d - gregorian.GregorianDate.days_in_year(year)
    else:
      gregorian_year = year
      ordinal_day = d
    
    return gregorian.GregorianDate.from_ordinal_date(gregorian_year, ordinal_day).days_since_epoch
  
  @classmethod
  def days_since_epoch_to_date[T: Integral](cls, days_since_epoch: T) -> tuple[T, T, T]:
    # https://en.wikipedia.org/wiki/ISO_week_date#Algorithms
    gregorian_date = gregorian.GregorianDate(days_since_epoch)
    ordinal_date = gregorian_date.ordinal_date()
    iso_day_of_week = gregorian_date.iso_day_of_week()
    year = gregorian_date.year
    week_number = (ordinal_date - iso_day_of_week + 10) // cls.DAYS_IN_WEEK
    
    if week_number < 1:
      year -= 1
      week_number = cls.weeks_in_year(gregorian_date.year - 1)
    elif week_number > cls.weeks_in_year(gregorian_date.year):
      if cls.weeks_in_year(gregorian_date.year) != 53:
        year += 1
        week_number = 1
    
    return year, week_number, iso_day_of_week
  
  @classmethod
  def parse_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-WXX-DD" or "-YYYY-WXX-DD" to date tuple.'
    match = cls._date_iso_string_regex.match(string)
    return int(match[1]), int(match[2]), int(match[3])
  
  # instance stuff
  
  __slots__ = '_year', '_week', '_day'
  _year: Integral
  _week: Integral
  _day: Integral
  
  def __init__(self, *args: tuple['str | Integral | DateBase | datetime_date_cls'] | tuple[Integral, Integral, Integral]):
    if len(args) == 1:
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
      elif isinstance(args[0], datetime_date_cls):
        datetime_date = args[0]
        self._days_since_epoch = self.__class__.from_datetime_date(datetime_date)._days_since_epoch
        self._year, self._week, self._day = self.days_since_epoch_to_date(self._days_since_epoch)
      else:
        raise TypeError(f'Unrecognized single argument {args[0]!r}')
    elif len(args) == 3:
      year, week, day = args
      
      weeks_in_year = self.weeks_in_year(year)
      
      if not (1 <= week <= weeks_in_year):
        raise ValueError(f'week {year}-W{week} out of range, must be between 1 and {weeks_in_year}')
      
      if not (1 <= day <= self.DAYS_IN_WEEK):
        raise ValueError(f'day {day} out of range, must be between 1 and {self.DAYS_IN_WEEK}')
      
      self._days_since_epoch = self.date_to_days_since_epoch(year, week, day)
      self._year = year
      self._week = week
      self._day = day
    else:
      raise TypeError(f'{self.__class__.__name__} constructor takes 1 or 3 arguments ({len(args)} given)')
  
  @classmethod
  def from_iso_string(cls, string: str) -> Self:
    'Converts a string in format "YYYY-WXX-DD" or "-YYYY-WXX-DD" to date object.'
    return cls(*cls.parse_iso_string(string))
  
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
    return (self.year, self.week, self.day)
  
  def to_iso_string(self) -> str:
    return f'{self.year}-W{self.week:0>2}-{self.day}'
