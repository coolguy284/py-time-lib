from enum import Enum
from re import compile as re_compile
from typing import Self

from ...fixed_prec import FixedPrec
from ...calendars.gregorian import GregorianDate
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.iso_weekdate import IsoWeekDate
from ..time_zone import TimeZone
from ..lib import TimeStorageType
from .time_inst_mono import TimeInstMonotonic

class TimeInstantFormatString(TimeInstMonotonic):
  # static stuff
  
  FORMAT_STRING_MAX_DIGITS = 1000
  
  _str_offset_to_fixedprec_minute = re_compile(r'([+-])(\d{2})(\d{2})')
  _str_offset_to_fixedprec_any = re_compile(r'([+-])(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?')
  
  @classmethod
  def fixedprec_offset_to_str(cls, offset_secs: TimeStorageType, minute_colon: bool = False) -> str:
    offset_secs = FixedPrec.from_basic(offset_secs)
    offset_sign = '+' if offset_secs >= 0 else '-'
    offset_hrs, remainder = divmod(abs(offset_secs), cls.NOMINAL_SECS_PER_HOUR)
    offset_mins, remainder = divmod(remainder, cls.NOMINAL_SECS_PER_MIN)
    offset_secs_trunc, offset_frac_secs = divmod(remainder, 1)
    
    if offset_frac_secs != 0:
      return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}.{str(offset_frac_secs.reduce_to_lowest_place()).split('.')[1]}'
    elif offset_secs_trunc != 0:
      return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}'
    elif offset_mins != 0 or offset_hrs != 0:
      if minute_colon:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}'
      else:
        return f'{offset_sign}{int(offset_hrs):0>2}{int(offset_mins):0>2}'
    else:
      if minute_colon:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}'
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
      raise ValueError('Offset string cannot be converted, form invalid')
  
  _format_string_state = Enum('_format_string_state', (
    'START',
    'PERCENT_START',
    'PERCENT_COLON',
    'FRAC_HIGH_PREC',
  ))
  
  @classmethod
  def format_string_from_info(cls, info: dict, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    state = cls._format_string_state.START
    result = ''
    
    for char in format_str:
      match state:
        case cls._format_string_state.START:
          if char == '%':
            state = cls._format_string_state.PERCENT_START
          else:
            result += char
        
        case cls._format_string_state.PERCENT_START:
          # C89 format strings
          if char == '%':
            result += '%'
          elif char == 'a':
            result += date_cls.WEEK_NAMES_SHORT[info['day_of_week']]
          elif char == 'A':
            result += date_cls.WEEK_NAMES_LONG[info['day_of_week']]
          elif char == 'b':
            result += date_cls.MONTH_NAMES_SHORT[info['month'] - 1]
          elif char == 'B':
            result += date_cls.MONTH_NAMES_LONG[info['month'] - 1]
          elif char == 'c':
            result += cls.format_string_from_info(info, '%a %b %d %H:%M:%S %Y', date_cls = date_cls)
          elif char == 'd':
            result += f'{info['day']:0>2}'
          elif char == 'f':
            result += f'{int(info['frac_second'] * cls.NOMINAL_MICROSECS_PER_SEC):0>6}'
          elif char == 'H':
            result += f'{info['hour']:0>2}'
          elif char == 'I':
            result += f'{(info['hour'] - 1) % 12 + 1:0>2}'
          elif char == 'j':
            result += f'{info['ordinal_day']:0>3}'
          elif char == 'm':
            result += f'{info['month']:0>2}'
          elif char == 'M':
            result += f'{info['minute']:0>2}'
          elif char == 'p':
            result += 'PM' if info['hour'] >= 12 else 'AM'
          elif char == 'S':
            result += f'{info['second']:0>2}'
          elif char == 'U':
            week_1_sunday_start_ordinal = date_cls.from_month_week_day(info['year'], 1, 1, 0).ordinal_date()
            week_num = (info['ordinal_day'] - week_1_sunday_start_ordinal) // date_cls.DAYS_IN_WEEK + 1
            result += f'{week_num:0>2}'
          elif char == 'w':
            result += str(info['day_of_week'])
          elif char == 'W':
            week_1_monday_start_ordinal = date_cls.from_month_week_day(info['year'], 1, 1, 1).ordinal_date()
            week_num = (info['ordinal_day'] - week_1_monday_start_ordinal) // date_cls.DAYS_IN_WEEK + 1
            result += f'{week_num:0>2}'
          elif char == 'x':
            result += cls.format_string_from_info(info, '%m/%d/%y', date_cls = date_cls)
          elif char == 'X':
            result += cls.format_string_from_info(info, '%H:%M:%S', date_cls = date_cls)
          elif char == 'y':
            result += f'{info['year'] % 100:0>2}'
          elif char == 'Y':
            if info['year'] < 0:
              result += f'-{-info['year']:0>3}'
            else:
              result += f'{info['year']:0>4}'
          elif char == 'z':
            result += cls.fixedprec_offset_to_str(info['tz_offset'])
          elif char == 'Z':
            result += info['tz_name']
          # datetime format strings
          elif char == 'G':
            result += f'{info['iso_week_date_year']:0>4}'
          elif char == 'u':
            result += str(info['iso_week_date_day'])
          elif char == 'V':
            result += f'{info['iso_week_date_week']:0>2}'
          elif char == ':':
            state = cls._format_string_state.PERCENT_COLON
            continue
          # custom format strings
          elif char == '.':
            state = cls._format_string_state.FRAC_HIGH_PREC
            frac_size = ''
            continue
          # invalid format specifier
          else:
            raise ValueError(f'Invalid format string sequence %{char}')
          
          state = cls._format_string_state.START
        
        case cls._format_string_state.PERCENT_COLON:
          # datetime format strings
          if char == 'z':
            result += cls.fixedprec_offset_to_str(info['tz_offset'], minute_colon = True)
          # invalid format specifier
          else:
            raise ValueError(f'Invalid format string sequence %:{char}')
          
          state = cls._format_string_state.START
        
        case cls._format_string_state.FRAC_HIGH_PREC:
          # custom format strings
          if char.isnumeric():
            frac_size += char
          elif char == 'f':
            frac_size = int(frac_size)
            if frac_size > cls.FORMAT_STRING_MAX_DIGITS:
              raise ValueError(f'Format string sequence %.{frac_size}f percision too large')
            else:
              result += f'{int(info['frac_second'] * 10 ** frac_size):0>{frac_size}}'
              state = cls._format_string_state.START
          # invalid format specifier
          else:
            raise ValueError(f'Invalid format string sequence %.{char}')
    
    return result
  
  # static stuff
  
  __slots__ = ()
  
  @classmethod
  def from_format_string_tai(cls, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def from_format_string_utc(cls, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def from_format_string_tz(cls, time_zone: TimeZone, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def from_format_string_mono(cls, time_scale: TimeInstMonotonic.TIME_SCALES, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  def to_format_string_tai(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a TAI time string formatted in the strftime style.'
    
    date = self.get_date_object_tai(date_cls = date_cls)
    year, month, day, hour, minute, second, frac_second = self.to_date_tuple_tai(date_cls = date_cls)
    day_of_week = date.day_of_week()
    ordinal_day = date.ordinal_date()
    iso_date = IsoWeekDate(date)
    
    return self.format_string_from_info({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'second': second,
      'frac_second': frac_second,
      'day_of_week': day_of_week,
      'ordinal_day': ordinal_day,
      'tz_offset': -self.get_utc_tai_offset(),
      'tz_name': 'Time Atomic International',
      'iso_week_date_year': iso_date.year,
      'iso_week_date_week': iso_date.week,
      'iso_week_date_day': iso_date.day,
    }, format_str, date_cls = date_cls)
  
  def to_format_string_utc(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a UTC time string formatted in the strftime style.'
    
    date = self.get_date_object_utc(date_cls = date_cls)
    year, month, day, hour, minute, second, frac_second = self.to_date_tuple_utc(date_cls = date_cls)
    day_of_week = date.day_of_week()
    ordinal_day = date.ordinal_date()
    iso_date = IsoWeekDate(date)
    
    return self.format_string_from_info({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'second': second,
      'frac_second': frac_second,
      'day_of_week': day_of_week,
      'ordinal_day': ordinal_day,
      'tz_offset': 0,
      'tz_name': 'Universal Time Coordinated',
      'iso_week_date_year': iso_date.year,
      'iso_week_date_week': iso_date.week,
      'iso_week_date_day': iso_date.day,
    }, format_str, date_cls = date_cls)
  
  def to_format_string_tz(self, time_zone: TimeZone, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a timezone time string formatted in the strftime style.'
    
    date = self.get_date_object_tz(time_zone, date_cls = date_cls)
    year, month, day, hour, minute, second, frac_second, _ = self.to_date_tuple_tz(time_zone, date_cls = date_cls)
    day_of_week = date.day_of_week()
    ordinal_day = date.ordinal_date()
    tz_offset, tz_offset_abbr = self.get_current_tz_offset(time_zone, date_cls = date_cls)
    iso_date = IsoWeekDate(date)
    
    return self.format_string_from_info({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'second': second,
      'frac_second': frac_second,
      'day_of_week': day_of_week,
      'ordinal_day': ordinal_day,
      'tz_offset': tz_offset,
      'tz_name': 'NULL' if tz_offset_abbr == None else tz_offset_abbr,
      'iso_week_date_year': iso_date.year,
      'iso_week_date_week': iso_date.week,
      'iso_week_date_day': iso_date.day,
    }, format_str, date_cls = date_cls)
  
  def to_format_string_mono(self, time_scale: TimeInstMonotonic.TIME_SCALES, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a monotonic-time-scale time string formatted in the strftime style.'
    
    date = self.get_date_object_mono(time_scale, date_cls = date_cls)
    year, month, day, hour, minute, second, frac_second = self.to_date_tuple_mono(time_scale, date_cls = date_cls)
    day_of_week = date.day_of_week()
    ordinal_day = date.ordinal_date()
    iso_date = IsoWeekDate(date)
    
    return self.format_string_from_info({
      'year': year,
      'month': month,
      'day': day,
      'hour': hour,
      'minute': minute,
      'second': second,
      'frac_second': frac_second,
      'day_of_week': day_of_week,
      'ordinal_day': ordinal_day,
      'tz_offset': -self.get_utc_tai_offset() + self.get_mono_tai_offset(time_scale),
      'tz_name': time_scale.name,
      'iso_week_date_year': iso_date.year,
      'iso_week_date_week': iso_date.week,
      'iso_week_date_day': iso_date.day,
    }, format_str, date_cls = date_cls)
