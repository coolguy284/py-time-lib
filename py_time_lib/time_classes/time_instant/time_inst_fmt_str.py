from re import compile as re_compile
from typing import Self

from ...fixed_prec import FixedPrec
from ...calendars.gregorian import GregorianDate
from ...calendars.jul_greg_base import JulGregBaseDate
from ..lib import TimeStorageType
from .time_inst_tz import TimeInstantTimeZones

class TimeInstantFormatString(TimeInstantTimeZones):
  # static stuff
  
  _str_offset_to_fixedprec_minute = re_compile(r'([+-])(\d{2})(\d{2})')
  _str_offset_to_fixedprec_any = re_compile(r'([+-])(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?')
  
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
  
  # static stuff
  
  __slots__ = ()
  
  @classmethod
  def from_format_string_tai(cls, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def from_format_string_utc(cls, format_str: str, time_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    raise NotImplementedError()
  
  def to_format_string_tai(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a time string formatted in the strftime style'
    
    percent_mode = False
    
    result = ''
    
    date = self.get_date_object_tai(date_cls = date_cls)
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
