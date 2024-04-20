from datetime import datetime, UTC as datetime_UTC
from numbers import Integral
from re import compile as re_compile
from time import time_ns
from typing import Self

from ...fixed_prec import FixedPrec
from ...data import leap_seconds
from ...calendars.date_base import DateBase
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.julian import JulianDate
from ...calendars.gregorian import GregorianDate
from ...auto_leap_seconds import DEFAULT_LEAP_FILE_PATH, DEFAULT_LEAP_FILE_URL, get_leap_sec_data
from ..lib import TimeStorageType
from .time_inst_leap_sec import TimeInstantLeapSec

class TimeInstant(TimeInstantLeapSec):
  'Class representing an instant of time. Modeled after TAI, with epoch at jan 1, 1 BCE (year 0). Stores seconds since epoch.'
  
  # static stuff
  
  # https://en.wikipedia.org/wiki/Julian_day
  JULIAN_DATE_ORIGIN_TUPLE: tuple[int, int, int, int, int, int, int] = -4712, 1, 1, 12, 0, 0, 0
  REDUCED_JULIAN_DATE_OFFSET_FROM_JD: FixedPrec = FixedPrec('-2400000')
  MODIFIED_JULIAN_DATE_OFFSET_FROM_JD: FixedPrec = FixedPrec('-2400000.5')
  
  _str_offset_to_fixedprec_minute = re_compile(r'([+-])(\d{2})(\d{2})')
  _str_offset_to_fixedprec_any = re_compile(r'([+-])(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?')
  
  @classmethod
  def epoch_instant_to_date_tuple(cls, secs_since_epoch: FixedPrec, date_cls: type[DateBase] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    days_since_epoch, time_since_day_start = divmod(secs_since_epoch, cls.NOMINAL_SECS_PER_DAY)
    date = date_cls.from_days_since_epoch(int(days_since_epoch))
    hour, remainder = divmod(time_since_day_start, cls.NOMINAL_SECS_PER_HOUR)
    minute, remainder = divmod(remainder, cls.NOMINAL_SECS_PER_MIN)
    second, frac_second = divmod(remainder, 1)
    return *date.to_date_tuple(), int(hour), int(minute), int(second), frac_second
  
  @classmethod
  def days_and_secs_to_mins_since_epoch(cls, days_since_epoch: Integral, time_in_day: TimeStorageType) -> tuple[int, TimeStorageType]:
    mins_in_day, remainder_secs = divmod(time_in_day, cls.NOMINAL_SECS_PER_MIN)
    return days_since_epoch * cls.NOMINAL_MINS_PER_DAY + int(mins_in_day), remainder_secs
  
  @classmethod
  def mins_to_days_and_secs_since_epoch(cls, mins_since_epoch: Integral, remainder_secs: TimeStorageType = FixedPrec(0)) -> tuple[int, TimeStorageType]:
    days_since_epoch, mins_in_day = divmod(mins_since_epoch, cls.NOMINAL_MINS_PER_DAY)
    return days_since_epoch, mins_in_day * cls.NOMINAL_SECS_PER_MIN + remainder_secs
  
  @classmethod
  def days_h_m_to_mins_since_epoch(cls, days_since_epoch: Integral, hour: Integral, minute: Integral) -> int:
    return days_since_epoch * cls.NOMINAL_MINS_PER_DAY + hour * cls.NOMINAL_MINS_PER_HOUR + minute
  
  @classmethod
  def mins_since_epoch_to_days_h_m(cls, mins_since_epoch: Integral) -> tuple[int, int, int]:
    hrs_since_epoch, minute = divmod(mins_since_epoch, cls.NOMINAL_MINS_PER_HOUR)
    days_since_epoch, hour = divmod(hrs_since_epoch, cls.NOMINAL_HOURS_PER_DAY)
    return days_since_epoch, hour, minute
  
  @classmethod
  def fixedprec_offset_to_str(cls, offset_secs: TimeStorageType) -> str:
    offset_sign = '+' if offset_secs >= 0 else '-'
    offset_hrs, remainder = divmod(abs(offset_secs), cls.NOMINAL_SECS_PER_HOUR)
    offset_mins, remainder = divmod(remainder, cls.NOMINAL_SECS_PER_MIN)
    offset_secs, offset_frac_secs = divmod(remainder, 1)
    
    if offset_frac_secs != 0:
      return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs):0>2}.{str(offset_frac_secs).split('.')[1]}'
    elif offset_secs != 0:
      return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs):0>2}'
    elif offset_mins != 0 or offset_hrs != 0:
      return f'{offset_sign}{int(offset_hrs):0>2}{int(offset_mins):0>2}'
    else:
      return 'Z'
  
  @classmethod
  def str_offset_to_fixedprec(cls, offset_str: str) -> FixedPrec:
    if offset_str == 'Z':
      return FixedPrec(0)
    elif match := cls._str_offset_to_fixedprec_minute.match(offset_str):
      return FixedPrec(
        int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
        int(match[3]) * cls.NOMINAL_SECS_PER_MIN
      ) * (1 if match[1] == '+' else -1)
    elif match := cls._str_offset_to_fixedprec_any.match(offset_str):
      if match[5] != None:
        return (
          int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
          int(match[3]) * cls.NOMINAL_SECS_PER_MIN +
          int(match[4]) +
          FixedPrec('0.' + match[5])
        ) * (1 if match[1] == '+' else -1)
      elif match[4] != None:
        return FixedPrec(
          int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
          int(match[3]) * cls.NOMINAL_SECS_PER_MIN +
          int(match[4])
        ) * (1 if match[1] == '+' else -1)
      else:
        return FixedPrec(
          int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
          int(match[3]) * cls.NOMINAL_SECS_PER_MIN
        ) * (1 if match[1] == '+' else -1)
    else:
      raise Exception('Offset string cannot be converted, form invalid')
  
  @classmethod
  def update_leap_seconds(cls, file_path = DEFAULT_LEAP_FILE_PATH, url = DEFAULT_LEAP_FILE_URL):
    leap_sec_data = get_leap_sec_data(file_path = file_path, url = url)
    leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI = leap_sec_data['initial_utc_tai_offset']
    leap_seconds.LEAP_SECONDS = leap_sec_data['leap_seconds']
    cls.UTC_INITIAL_OFFSET_FROM_TAI = leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI
    cls.LEAP_SECONDS = leap_seconds.LEAP_SECONDS
    cls._init_class_vars()
  
  @classmethod
  def _init_class_vars(cls) -> None:
    # https://stackoverflow.com/questions/1817183/using-super-with-a-class-method/47247072#47247072
    super()._init_class_vars()
    
    # basic functionality of TimeInstant created by this point so TimeInstant methods can be called
    
    cls.UNIX_TIMESTAMP_ORIGIN_OFFSET: TimeStorageType = cls.from_date_tuple_utc(1970, 1, 1, 0, 0, 0, 0).to_utc_secs_since_epoch()[0]
    cls.JULIAN_DATE_OFFSET: TimeStorageType = cls.from_date_tuple_tai(*cls.JULIAN_DATE_ORIGIN_TUPLE, date_cls = JulianDate).time
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_date_tuple_tai(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, date_cls: type[DateBase] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a tai TimeInstant.'
    date = date_cls(year, month, day)
    time = date.days_since_epoch * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    return cls(time)
  
  @classmethod
  def from_date_tuple_utc(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, round_invalid_time_upwards: bool = True, date_cls: type[DateBase] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a utc TimeInstant. Does not handle leap seconds that occur during the day.'
    date = date_cls(year, month, day)
    time = date.days_since_epoch * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    date_mins = cls.days_h_m_to_mins_since_epoch(date.days_since_epoch, hour, minute)
    if date_mins in cls.LEAP_SECONDS_DICT:
      leap_entries = cls.LEAP_SECONDS_DICT[date_mins]
      leap_delta = leap_entries[-1]['utc_delta']
      if leap_delta < 0:
        # positive leap second
        if hour * cls.NOMINAL_SECS_PER_HOUR + minute * cls.NOMINAL_SECS_PER_MIN + second + frac_second < -leap_delta:
          leap_fold = True
        else:
          leap_fold = False
      else:
        leap_fold = False
    else:
      leap_fold = False
    return TimeInstant.from_utc_secs_since_epoch(time, second_fold = leap_fold, round_invalid_time_upwards = round_invalid_time_upwards)
  
  @classmethod
  def from_unix_timestamp(cls, unix_secs_since_epoch: TimeStorageType, second_fold: bool = False) -> Self:
    return cls.from_utc_secs_since_epoch(unix_secs_since_epoch + cls.UNIX_TIMESTAMP_ORIGIN_OFFSET, second_fold)
  
  @classmethod
  def from_julian_date_tai(cls, julian_date: TimeStorageType) -> Self:
    return cls((julian_date * cls.NOMINAL_SECS_PER_DAY) + cls.JULIAN_DATE_OFFSET)
  
  @classmethod
  def from_reduced_julian_date_tai(cls, reduced_julian_date: TimeStorageType) -> Self:
    return cls.from_julian_date_tai(reduced_julian_date - cls.REDUCED_JULIAN_DATE_OFFSET_FROM_JD)
  
  @classmethod
  def from_modified_julian_date_tai(cls, modified_julian_date: TimeStorageType) -> Self:
    return cls.from_julian_date_tai(modified_julian_date - cls.MODIFIED_JULIAN_DATE_OFFSET_FROM_JD)
  
  @classmethod
  def from_format_string_tai(cls, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def from_format_string_utc(cls, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def now(cls) -> Self:
    return cls.from_unix_timestamp(FixedPrec(time_ns(), 9))
  
  def to_date_tuple_tai(self, date_cls: type[DateBase] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    'Returns a date tuple in the TAI timezone (as math is easiest for this).'
    return self.epoch_instant_to_date_tuple(self._time, date_cls = date_cls)
  
  def to_date_tuple_utc(self, date_cls: type[DateBase] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    'Returns a date tuple in the UTC timezone. Does not handle leap seconds that occur during the day.'
    utc_info = self.to_utc_info()
    utc_secs_since_epoch = utc_info['utc_seconds_since_epoch']
    if utc_info['positive_leap_second_occurring']:
      utc_secs_since_epoch -= 1
    *date, hour, minute, second, frac_second = self.epoch_instant_to_date_tuple(utc_secs_since_epoch, date_cls = date_cls)
    if utc_info['positive_leap_second_occurring']:
      second += 1
      second_addl, frac_second = divmod(frac_second + (self._time - utc_info['last_leap_transition_time']), 1)
      second = int(second + second_addl)
    return *date, hour, minute, second, frac_second
  
  def to_unix_timestamp(self) -> tuple[TimeStorageType, bool]:
    '''
    Returns a unix timestamp tuple in the form of (unix_secs_since_epoch, second_fold).
    After a positive leap second, the counter gets set back one second and second_fold
    becomes true for one second.
    '''
    utc_secs_since_epoch, second_fold = self.to_utc_secs_since_epoch()
    unix_secs_since_epoch = utc_secs_since_epoch - self.UNIX_TIMESTAMP_ORIGIN_OFFSET
    return unix_secs_since_epoch, second_fold
  
  def to_julian_date_tai(self) -> TimeStorageType:
    return (self.time - self.JULIAN_DATE_OFFSET) / self.NOMINAL_SECS_PER_DAY
  
  def to_reduced_julian_date_tai(self) -> TimeStorageType:
    return self.to_julian_date_tai() + self.REDUCED_JULIAN_DATE_OFFSET_FROM_JD
  
  def to_modified_julian_date_tai(self) -> TimeStorageType:
    return self.to_julian_date_tai() + self.MODIFIED_JULIAN_DATE_OFFSET_FROM_JD
  
  def get_utc_tai_offset(self) -> FixedPrec:
    return self.to_utc_info()['current_utc_tai_offset']
  
  def get_date_object[T: DateBase](self, date_cls: type[T] = GregorianDate) -> T:
    days_since_epoch, _ = divmod(self.time, self.NOMINAL_SECS_PER_DAY)
    return date_cls.from_days_since_epoch(int(days_since_epoch))
  
  def to_format_string_tai(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a time string formatted in the strftime style'
    
    percent_mode = False
    
    result = ''
    
    date = self.get_date_object(date_cls = date_cls)
    year, month, day, hour, minute, second, frac_second = self.to_date_tuple_tai(date_cls = date_cls)
    day_of_week = date.day_of_week()
    ordinal_day = date.ordinal_date()
    
    for char in format_str:
      if not percent_mode:
        if char == '%':
          percent_mode = True
        else:
          result += char
      else:
        if char == '%':
          result += '%'
        elif char == 'a':
          result += date.WEEK_NAMES_SHORT[day_of_week]
        elif char == 'A':
          result += date.WEEK_NAMES_LONG[day_of_week]
        elif char == 'b':
          result += date.MONTH_NAMES_SHORT[month - 1]
        elif char == 'B':
          result += date.MONTH_NAMES_LONG[month - 1]
        elif char == 'c':
          result += self.to_format_string_tai('%a %b %d %H:%M:%S %Y')
        elif char == 'd':
          result += f'{day:0>2}'
        elif char == 'f':
          result += f'{int(frac_second * 1_000_000):0>2}'
        elif char == 'H':
          result += f'{hour:0>2}'
        elif char == 'I':
          result += f'{(hour - 1) % 12 + 1:0>2}'
        elif char == 'j':
          result += f'{ordinal_day:0>3}'
        elif char == 'm':
          result += f'{month:0>2}'
        elif char == 'M':
          result += f'{minute:0>2}'
        elif char == 'p':
          result += 'PM' if hour >= 12 else 'AM'
        elif char == 'S':
          result += f'{second:0>2}'
        elif char == 'U':
          week_1_start_ordinal = date_cls.from_month_week_day(year, 1, 1, 0).ordinal_date()
          week_num = (ordinal_day - week_1_start_ordinal) // date_cls.DAYS_IN_WEEK + 1
          result += f'{week_num:0>2}'
        elif char == 'w':
          result += str(day_of_week)
        elif char == 'W':
          week_1_start_ordinal = date_cls.from_month_week_day(year, 1, 1, 1).ordinal_date()
          week_num = (ordinal_day - week_1_start_ordinal) // date_cls.DAYS_IN_WEEK + 1
          result += f'{week_num:0>2}'
        elif char == 'x':
          result += self.to_format_string_tai('%m/%d/%y')
        elif char == 'X':
          result += self.to_format_string_tai('%H:%M:%S')
        elif char == 'y':
          result += f'{year % 100:0>2}'
        elif char == 'Y':
          result += str(year)
        elif char == 'z':
          result += self.fixedprec_offset_to_str(-self.get_utc_tai_offset())
        elif char == 'Z':
          result += 'Time Atomic International'
        else:
          raise ValueError(f'Invalid format string sequence %{char}')
        percent_mode = False
    
    return result
  
  def to_format_string_utc(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    raise NotImplementedError()
  
  strftime = to_format_string_tai
  
  def to_datetime(self) -> datetime:
    utc_info = self.to_utc_info()
    if utc_info['positive_leap_second_occurring']:
      self_adjusted = self.__class__.from_utc_secs_since_epoch(utc_info['utc_seconds_since_epoch'], True)
    else:
      self_adjusted = self
    
    year, month, day, hour, minute, second, frac_second = self_adjusted.to_date_tuple_utc()
    
    return datetime(year, month, day, hour, minute, second, int(frac_second * self.NOMINAL_MICROSECS_PER_SEC), datetime_UTC)

TimeInstant._init_class_vars()
