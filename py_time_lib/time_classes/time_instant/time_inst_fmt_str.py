from enum import Enum
from numbers import Integral
from re import compile as re_compile
from typing import Self

from ...fixed_prec import FixedPrec
from ...constants import NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX, YEARS_IN_CENTURY, NOMINAL_DAYS_PER_WEEK
from ...calendars.gregorian import GregorianDate
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.iso_weekdate import IsoWeekDate
from ..time_zone import TimeZone
from ..lib import TimeStorageType
from .time_inst_solar import TimeInstantSolar
from .time_inst_smear import LeapSmearPlan, TimeInstantLeapSmear
from ...named_tuples import DateTupleBasic, DateTupleFormatString

class TimeInstantFormatString(TimeInstantSolar, TimeInstantLeapSmear):
  # static stuff
  
  FORMAT_STRING_MAX_DIGITS = 1000
  HALF_DAY_VARIATIONS = ('AM', 'PM')
  DEFAULT_TIMEZONE_NAME = 'NULL'
  
  _str_offset_to_fixedprec_minute = re_compile(r'^([+-])(\d{2})(\d{2})')
  _str_offset_to_fixedprec_any = re_compile(r'^([+-])(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?')
  
  @classmethod
  def fixedprec_offset_to_str(cls, offset_secs: TimeStorageType, minute_colon: bool = False, precision: Integral | None = None) -> str:
    'Precision can be -1 to truncate to minute.'
    
    offset_secs = FixedPrec.from_basic(offset_secs)
    offset_sign = '+' if offset_secs >= 0 else '-'
    offset_hrs, remainder = divmod(abs(offset_secs), cls.NOMINAL_SECS_PER_HOUR)
    offset_mins, remainder = divmod(remainder, cls.NOMINAL_SECS_PER_MIN)
    offset_secs_trunc, offset_frac_secs = divmod(remainder, 1)
    
    if precision != None:
      if precision == -1:
        if minute_colon:
          result = f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}'
          
          if result == '-00:00':
            return '+00:00'
          else:
            return result
        else:
          if offset_secs == 0:
            return 'Z'
          else:
            result = f'{offset_sign}{int(offset_hrs):0>2}{int(offset_mins):0>2}'
            
            if result == '-0000':
              return '+0000'
            else:
              return result
      elif precision == 0:
        result = f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}'
        
        if result == '-00:00:00':
          return '+00:00:00'
        else:
          return result
      else:
        frac_sec_split = str(offset_frac_secs.reduce_to_lowest_place()).split('.')
        
        if len(frac_sec_split) > 1:
          frac_sec_str = frac_sec_split[1][:precision]
        else:
          frac_sec_str = ''
        
        result = f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}.{frac_sec_str:0<{precision}}'
        
        if result == f'-00:00:00.{'0' * precision}':
          return f'+00:00:00.{'0' * precision}'
        else:
          return result
    elif minute_colon:
      if offset_frac_secs != 0:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}.{str(offset_frac_secs.reduce_to_lowest_place()).split('.')[1]}'
      elif offset_secs_trunc != 0:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}'
      elif offset_mins != 0 or offset_hrs != 0:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}'
      else:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}'
    else:
      if offset_frac_secs != 0:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}.{str(offset_frac_secs.reduce_to_lowest_place()).split('.')[1]}'
      elif offset_secs_trunc != 0:
        return f'{offset_sign}{int(offset_hrs):0>2}:{int(offset_mins):0>2}:{int(offset_secs_trunc):0>2}'
      elif offset_mins != 0 or offset_hrs != 0:
        return f'{offset_sign}{int(offset_hrs):0>2}{int(offset_mins):0>2}'
      else:
        return 'Z'
  
  @classmethod
  def str_offset_to_fixedprec(cls, offset_str: str, allow_text_beyond_end: bool = False) -> FixedPrec | tuple[FixedPrec, int]:
    'If text beyond end is allowed, return value is tuple of offset and length of characters parsed.'
    if not allow_text_beyond_end:
      offset, length = cls.str_offset_to_fixedprec(offset_str, allow_text_beyond_end = True)
      if len(offset_str) > length:
        raise ValueError('Offset string cannot be converted, extra content beyond end of offset')
      else:
        return offset
    else:
      if offset_str[0:1] == 'Z':
        return FixedPrec(0), 1
      elif match := cls._str_offset_to_fixedprec_minute.match(offset_str):
        return (
          FixedPrec(
            int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
            int(match[3]) * cls.NOMINAL_SECS_PER_MIN
          ) * (1 if match[1] == '+' else -1),
          len(match[1]) + len(match[2]) + len(match[3]),
        )
      elif match := cls._str_offset_to_fixedprec_any.match(offset_str):
        if match[5] != None:
          return (
            (
              int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
              int(match[3]) * cls.NOMINAL_SECS_PER_MIN +
              int(match[4]) +
              FixedPrec('0.' + match[5])
            ) * (1 if match[1] == '+' else -1),
            len(match[1]) + len(match[2]) + 1 + len(match[3]) + 1 + len(match[4]) + 1 + len(match[5]),
          )
        elif match[4] != None:
          return (
            FixedPrec(
              int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
              int(match[3]) * cls.NOMINAL_SECS_PER_MIN +
              int(match[4])
            ) * (1 if match[1] == '+' else -1),
            len(match[1]) + len(match[2]) + 1 + len(match[3]) + 1 + len(match[4]),
          )
        else:
          return (
            FixedPrec(
              int(match[2]) * cls.NOMINAL_SECS_PER_HOUR +
              int(match[3]) * cls.NOMINAL_SECS_PER_MIN
            ) * (1 if match[1] == '+' else -1),
            len(match[1]) + len(match[2]) + 1 + len(match[3]),
          )
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
            result += info['tz_name'] if info['tz_name'] != None else cls.DEFAULT_TIMEZONE_NAME
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
            minute_colon = None
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
            if minute_colon == True:
              raise ValueError('Format specifier has numbers after minute colon')
            elif frac_size == 'm':
              raise ValueError('Format specifier number invalid')
            else:
              frac_size += char
          elif char == 'm':
            if minute_colon == True:
              raise ValueError('Format specifier has information after minute colon')
            elif frac_size != '':
              raise ValueError('Format specifier number invalid')
            else:
              frac_size += char
          elif char == ':':
            if minute_colon == True:
              raise ValueError('Format specifier has double minute colon')
            else:
              minute_colon = True
          elif char == 'f':
            if minute_colon == True:
              raise ValueError(f'Format specifier %.{frac_size}:f invalid')
            elif frac_size == '':
              place = info['frac_second'].place
              result += f'{int(info['frac_second'] * 10 ** place):0>{place}}'
            elif frac_size == 'm':
              raise ValueError(f'Format string sequence %.{frac_size}f invalid')
            else:
              frac_size = int(frac_size)
              if frac_size > cls.FORMAT_STRING_MAX_DIGITS:
                raise ValueError(f'Format string sequence %.{frac_size}f percision too large')
              else:
                result += f'{int(info['frac_second'] * 10 ** frac_size):0>{frac_size}}'
            state = cls._format_string_state.START
          elif char == 'z':
            minute_colon = True if minute_colon == True else False
            if frac_size == '':
              result += cls.fixedprec_offset_to_str(info['tz_offset'], minute_colon = minute_colon)
            elif frac_size == 'm':
              result += cls.fixedprec_offset_to_str(info['tz_offset'], minute_colon = minute_colon, precision = -1)
            else:
              frac_size = int(frac_size)
              if frac_size > cls.FORMAT_STRING_MAX_DIGITS:
                raise ValueError(f'Format string sequence %.{frac_size}z percision too large')
              else:
                result += cls.fixedprec_offset_to_str(info['tz_offset'], minute_colon = minute_colon, precision = frac_size)
            state = cls._format_string_state.START
          # invalid format specifier
          else:
            raise ValueError(f'Invalid format string sequence %.{frac_size}{char}')
    
    return result
  
  @classmethod
  def get_string_array_match(cls, format_arr: list[str], string: str) -> int | None:
    for i in range(len(format_arr)):
      test_str = format_arr[i]
      if string.startswith(test_str):
        return i
    
    return None
  
  @classmethod
  def info_from_format_string(
      cls,
      format_str: str,
      time_str: str,
      error_if_invalid_base_char: bool = True,
      error_if_time_str_too_long: bool = True,
      date_cls: type[JulGregBaseDate] = GregorianDate
    ) -> tuple[dict, int]:
    'Return argument is format string info dict, then int of length of format string copied.'
    
    state = cls._format_string_state.START
    index = 0
    info = {}
    
    for char in format_str:
      match state:
        case cls._format_string_state.START:
          if char == '%':
            state = cls._format_string_state.PERCENT_START
          else:
            if time_str[index] == char or not error_if_invalid_base_char:
              pass
            else:
              raise ValueError(f'Character mismatch at char {index}, expected {char}, found {time_str[index]}')
            
            index += 1
        
        case cls._format_string_state.PERCENT_START:
          # C89 format strings
          if char == '%':
            if time_str[index] == char or not error_if_invalid_base_char:
              pass
            else:
              raise ValueError(f'Character mismatch at char {index}, expected {char}, found {time_str[index]}')
            
            index += 1
          elif char == 'a':
            day_of_week = cls.get_string_array_match(date_cls.WEEK_NAMES_SHORT, time_str[index:])
            if day_of_week == None:
              raise ValueError(f'Day of week invalid: {time_str[index:]}')
            else:
              info['day_of_week'] = day_of_week
            
            index += len(date_cls.WEEK_NAMES_SHORT[day_of_week])
          elif char == 'A':
            day_of_week = cls.get_string_array_match(date_cls.WEEK_NAMES_LONG, time_str[index:])
            if day_of_week == None:
              raise ValueError(f'Day of week invalid: {time_str[index:]}')
            else:
              info['day_of_week'] = day_of_week
            
            index += len(date_cls.WEEK_NAMES_LONG[day_of_week])
          elif char == 'b':
            month_of_year = cls.get_string_array_match(date_cls.MONTH_NAMES_SHORT, time_str[index:])
            if month_of_year == None:
              raise ValueError(f'Month of year invalid: {time_str[index:]}')
            else:
              info['day_of_week'] = month_of_year + 1
            
            index += len(date_cls.MONTH_NAMES_SHORT[day_of_week])
          elif char == 'B':
            month_of_year = cls.get_string_array_match(date_cls.MONTH_NAMES_LONG, time_str[index:])
            if month_of_year == None:
              raise ValueError(f'Month of year invalid: {time_str[index:]}')
            else:
              info['day_of_week'] = month_of_year + 1
            
            index += len(date_cls.MONTH_NAMES_LONG[day_of_week])
          elif char == 'c':
            new_info, length = cls.info_from_format_string(
              format_str = '%a %b %d %H:%M:%S %Y',
              time_str = time_str[index:],
              error_if_invalid_base_char = error_if_invalid_base_char,
              error_if_time_str_too_long = False,
              date_cls = date_cls
            )
            
            info.update(new_info)
            
            index += length
          elif char == 'd':
            info['day'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'f':
            info['frac_second'] = FixedPrec(int(time_str[index:index + 6]), NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX)
            index += 6
          elif char == 'H':
            info['hour'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'I':
            info['12hr_hour'] = int(time_str[index:index + 2]) % 12
            index += 2
          elif char == 'j':
            info['ordinal_day'] = int(time_str[index:index + 3])
            index += 3
          elif char == 'm':
            info['month'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'M':
            info['minute'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'p':
            half_day_variation = cls.get_string_array_match(cls.HALF_DAY_VARIATIONS, time_str[index:])
            info['12hr_half_day'] = half_day_variation
            index += len(cls.HALF_DAY_VARIATIONS[half_day_variation])
          elif char == 'S':
            info['second'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'U':
            info['week_num_sunday_start'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'w':
            info['day_of_week'] = int(time_str[index])
            index += 1
          elif char == 'W':
            info['week_num_monday_start'] = int(time_str[index:index + 2])
            index += 2
          elif char == 'x':
            new_info, length = cls.info_from_format_string(
              format_str = '%m/%d/%y',
              time_str = time_str[index:],
              error_if_invalid_base_char = error_if_invalid_base_char,
              error_if_time_str_too_long = False,
              date_cls = date_cls
            )
            
            info.update(new_info)
            
            index += length
          elif char == 'X':
            new_info, length = cls.info_from_format_string(
              format_str = '%H:%M:%S',
              time_str = time_str[index:],
              error_if_invalid_base_char = error_if_invalid_base_char,
              error_if_time_str_too_long = False,
              date_cls = date_cls
            )
            
            info.update(new_info)
            
            index += length
          elif char == 'y':
            info['year_mod_100'] = int(time_str[index:index + 2]) % 12
            index += 2
          elif char == 'Y':
            if time_str[index] == '-':
              year_part = '-'
              index += 1
            else:
              year_part = ''
            
            while index < len(time_str) and time_str[index:index + 1].isdigit():
              year_part += time_str[index]
              index += 1
            
            info['year'] = int(year_part)
          elif char == 'z':
            offset, length = cls.str_offset_to_fixedprec(time_str[index:], allow_text_beyond_end = True)
            info['tz_offset'] = offset
            index += length
          elif char == 'Z':
            raise ValueError('Format string parse code %Z unsupported')
          # datetime format strings
          elif char == 'G':
            if time_str[index] == '-':
              year_part = '-'
              index += 1
            else:
              year_part = ''
            
            while index < len(time_str) and time_str[index:index + 1].isdigit():
              year_part += time_str[index]
              index += 1
            
            info['iso_week_date_year'] = int(year_part)
          elif char == 'u':
            info['iso_week_date_day'] = int(time_str[index])
            index += 1
          elif char == 'V':
            info['iso_week_date_week'] = int(time_str[index:index + 2])
            index += 2
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
            offset, length = cls.str_offset_to_fixedprec(time_str[index:], allow_text_beyond_end = True)
            info['tz_offset'] = offset
            index += length
          # invalid format specifier
          else:
            raise ValueError(f'Invalid format string sequence %:{char}')
          
          state = cls._format_string_state.START
        
        case cls._format_string_state.FRAC_HIGH_PREC:
          # custom format strings
          if char.isnumeric():
            if minute_colon == True:
              raise ValueError('Format specifier has numbers after minute colon')
            elif frac_size == 'm':
              raise ValueError('Format specifier number invalid')
            else:
              frac_size += char
          elif char == 'm':
            if minute_colon == True:
              raise ValueError('Format specifier has information after minute colon')
            elif frac_size != '':
              raise ValueError('Format specifier number invalid')
            else:
              frac_size += char
          elif char == ':':
            if minute_colon == True:
              raise ValueError('Format specifier has double minute colon')
            else:
              minute_colon = True
          elif char == 'f':
            if minute_colon == True:
              raise ValueError(f'Format specifier %.{frac_size}:f invalid')
            elif frac_size == '':
              frac_part = ''
              
              while index < len(time_str) and time_str[index:index + 1].isdigit():
                frac_part += time_str[index]
                index += 1
              
              info['frac_second'] = FixedPrec(f'0.{frac_part}')
            elif frac_size == 'm':
              raise ValueError(f'Format string sequence %.{frac_size}f invalid')
            else:
              frac_size = int(frac_size)
              
              if frac_size > cls.FORMAT_STRING_MAX_DIGITS:
                raise ValueError(f'Format string sequence %.{frac_size}f percision too large')
              else:
                frac_part = time_str[index:index + frac_size]
                
                if frac_part.isdigit():
                  info['frac_second'] = FixedPrec(f'0.{frac_part}')
                  index += frac_size
                else:
                  raise ValueError(f'"{frac_part}" is not a digit string and is invalid for %f')
            state = cls._format_string_state.START
          elif char == 'z':
            minute_colon = True if minute_colon == True else False
            if frac_size == '':
              offset, length = cls.str_offset_to_fixedprec(time_str[index:], allow_text_beyond_end = True)
              info['tz_offset'] = offset
              index += length
            elif frac_size == 'm':
              offset, length = cls.str_offset_to_fixedprec(time_str[index:], allow_text_beyond_end = True)
              info['tz_offset'] = offset
              index += length
            else:
              frac_size = int(frac_size)
              if frac_size > cls.FORMAT_STRING_MAX_DIGITS:
                raise ValueError(f'Format string sequence %.{frac_size}z percision too large')
              else:
                offset, length = cls.str_offset_to_fixedprec(time_str[index:], allow_text_beyond_end = True)
                info['tz_offset'] = offset
                index += length
            state = cls._format_string_state.START
          # invalid format specifier
          else:
            raise ValueError(f'Invalid format string sequence %.{frac_size}{char}')
    
    if index < len(time_str) and error_if_time_str_too_long:
      raise ValueError(f'Time string extends {len(time_str) - index} chars past format string')
    
    return info, index
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def format_string_to_date_tuple(
    cls,
    format_str: str,
    date_cls: type[JulGregBaseDate],
    time_str: str,
    default_info: dict = {},
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True,
  ) -> DateTupleFormatString:
    info = default_info.copy()
    
    info.update(cls.info_from_format_string(
      format_str = format_str,
      time_str = time_str,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long,
      date_cls = date_cls
    )[0])
    
    # get year
    
    if 'year' in info:
      # gregorian year
      year = info['year']
      iso_week_date = False
    elif 'year_mod_100' in info:
      # gregorian year and century
      year = info['year_floordiv_100'] * YEARS_IN_CENTURY + info['year_mod_100']
      iso_week_date = False
    else:
      # iso week date
      iso_week_date = True
    
    # get date
    
    if iso_week_date:
      date = date_cls.from_iso_week_tuple(
        info['iso_week_date_year'],
        info['iso_week_date_week'],
        info['iso_week_date_day']
      )
    else:
      if 'month' in info:
        date = date_cls(year, info['month'], info['day'])
      elif 'ordinal_day' in info:
        date = date_cls.from_ordinal_date(year, info['ordinal_day'])
      elif 'week_num_sunday_start' in info:
        week_1_sunday_start_ordinal = date_cls.from_month_week_day(info['year'], 1, 1, 0).ordinal_date()
        ordinal_day = week_1_sunday_start_ordinal + \
          info['week_num_sunday_start'] * NOMINAL_DAYS_PER_WEEK + \
          info['day_of_week']
        date = date_cls.from_ordinal_date(year, ordinal_day)
      elif 'week_num_monday_start' in info:
        week_1_monday_start_ordinal = date_cls.from_month_week_day(info['year'], 1, 1, 1).ordinal_date()
        ordinal_day = week_1_monday_start_ordinal + \
          info['week_num_monday_start'] * NOMINAL_DAYS_PER_WEEK + \
          (info['day_of_week'] - 1) % NOMINAL_DAYS_PER_WEEK
        date = date_cls.from_ordinal_date(year, ordinal_day)
    
    # get hour
    
    if 'hour' in info:
      hour = info['hour']
    else:
      hour = info['12hr_half_day'] * 12 + info['12hr_hour']
    
    # get remaining values
    
    minute = info['minute']
    second = info['second']
    frac_second = info['frac_second']
    
    if 'tz_offset' in info:
      tz_offset = info['tz_offset']
    else:
      tz_offset = None
    
    return DateTupleFormatString(date.year, date.month, date.day, hour, minute, second, frac_second, tz_offset, None)
  
  @classmethod
  def from_format_string(
    cls,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> Self:
    '''
    Parses a time string with the given format string and default values into a TimeInstant.
    Possible default values:
    {
      calendar day (pick one):
        gregorian or similar:
          year (pick one):
            standard:
              'year': <any integer>, calendar year,
            
            century split:
              'year_floordiv_100': century number, century 0 is years 0 CE to 99 CE. must be manually set as default, cannot be parsed from format string,
              'year_mod_100': year without century,
          
          day in year (pick one):
            standard:
              'month': 0-12, month in year,
              'day': day in month,
            
            ordinal:
              'ordinal_day': 1-366 (typically), day in year,
            
            week numbered, sunday start:
              'week_num_sunday_start': 00-53, week number in year, week 1 starts on sunday and is first sunday of the year,
              'day_of_week': 0=sunday, 6=saturday,
            
            week numbered, monday start:
              'week_num_monday_start': 00-53, week number in year, week 1 starts on monday and is first monday of the year,
              'day_of_week': 0=sunday, 6=saturday,
        
        iso week date:
          'iso_week_date_year': year in the iso week date calendar,
          'iso_week_date_week': week of year in iso week date calendar,
          'iso_week_date_day': day of week, 1-7, 1=monday, 7=sunday,
      
      time in day:
        hour (pick one):
          standard (24 hour):
            'hour': hour in day,
          
          AM/PM (12 hour):
            '12hr_half_day': 0 or 1, 0 is 12am-11am, 1 is 12pm-11pm,
            '12hr_hour': 0-11, hour value in each half of the day (either before noon or after (and during) noon),
        
        remainder:
          'minute': 0-59, minute in hour,
          'second': 0-60, second in minute,
          'frac_second': FixedPrec fractional component of second, in range [0, 1),
      
      timezone:
        'tz_offset': FixedPrec timezone offset from UTC in seconds,
    }
    '''
    
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    return cls.from_date_tuple_tz(
      TimeZone(date_tup.tz_offset),
      date_tup.year,
      date_tup.month,
      date_tup.day,
      date_tup.hour,
      date_tup.minute,
      date_tup.second,
      date_tup.frac_second,
      dst_second_fold = False,
      date_cls = date_cls
    )
  
  @classmethod
  def from_format_string_tai(
    cls,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> Self:
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    return cls.from_date_tuple_tai(
      date_tup.year,
      date_tup.month,
      date_tup.day,
      date_tup.hour,
      date_tup.minute,
      date_tup.second,
      date_tup.frac_second,
      date_cls = date_cls
    )
  
  @classmethod
  def from_format_string_utc(
    cls,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> Self:
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    return cls.from_date_tuple_utc(
      date_tup.year,
      date_tup.month,
      date_tup.day,
      date_tup.hour,
      date_tup.minute,
      date_tup.second,
      date_tup.frac_second,
      date_cls = date_cls
    )
  
  @classmethod
  def from_format_string_tz(
    cls,
    time_zone: TimeZone,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> Self:
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    return cls.from_date_tuple_tz(
      time_zone,
      date_tup.year,
      date_tup.month,
      date_tup.day,
      date_tup.hour,
      date_tup.minute,
      date_tup.second,
      date_tup.frac_second,
      date_cls = date_cls
    )
  
  @classmethod
  def from_format_string_mono(
    cls,
    time_scale: TimeInstantSolar.TIME_SCALES,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> Self:
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    return cls.from_date_tuple_mono(
      time_scale,
      date_tup.year,
      date_tup.month,
      date_tup.day,
      date_tup.hour,
      date_tup.minute,
      date_tup.second,
      date_tup.frac_second,
      date_cls = date_cls
    )
  
  @classmethod
  def from_format_string_solar(
    cls,
    longitude_deg: TimeStorageType,
    true_solar_time: bool,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ):
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    return cls.from_date_tuple_solar(
      longitude_deg,
      true_solar_time,
      date_tup.year,
      date_tup.month,
      date_tup.day,
      date_tup.hour,
      date_tup.minute,
      date_tup.second,
      date_tup.frac_second,
      date_cls = date_cls
    )
  
  @classmethod
  def from_format_string_smear_utc(
    cls,
    smear_plan: LeapSmearPlan,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    true_utc_offset: bool = False,
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> str:
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    if true_utc_offset:
      return cls.from_date_tuple_tz(
        TimeZone(date_tup.tz_offset),
        date_tup.year,
        date_tup.month,
        date_tup.day,
        date_tup.hour,
        date_tup.minute,
        date_tup.second,
        date_tup.frac_second,
        date_cls = date_cls
      )
    else:
      return cls.from_date_tuple_smear_utc(
        smear_plan,
        date_tup.year,
        date_tup.month,
        date_tup.day,
        date_tup.hour,
        date_tup.minute,
        date_tup.second,
        date_tup.frac_second,
        date_cls = date_cls
      )
  
  @classmethod
  def from_format_string_smear_tz(
    cls,
    smear_plan: LeapSmearPlan,
    time_zone: TimeZone,
    format_str: str,
    time_str: str,
    default_info: dict = {},
    true_utc_offset: bool = False,
    date_cls: type[JulGregBaseDate] = GregorianDate,
    error_if_invalid_base_char: bool = True,
    error_if_time_str_too_long: bool = True
  ) -> str:
    date_tup = cls.format_string_to_date_tuple(
      format_str = format_str,
      date_cls = date_cls,
      time_str = time_str,
      default_info = default_info,
      error_if_invalid_base_char = error_if_invalid_base_char,
      error_if_time_str_too_long = error_if_time_str_too_long
    )
    
    if true_utc_offset:
      return cls.from_date_tuple_tz(
        TimeZone(date_tup.tz_offset),
        date_tup.year,
        date_tup.month,
        date_tup.day,
        date_tup.hour,
        date_tup.minute,
        date_tup.second,
        date_tup.frac_second,
        date_cls = date_cls
      )
    else:
      return cls.from_date_tuple_smear_tz(
        smear_plan,
        time_zone,
        date_tup.year,
        date_tup.month,
        date_tup.day,
        date_tup.hour,
        date_tup.minute,
        date_tup.second,
        date_tup.frac_second,
        date_cls = date_cls
      )
  
  @classmethod
  def date_tuple_to_format_string(cls, format_str: str, date_cls: type[JulGregBaseDate], date_tup: DateTupleFormatString) -> str:
    year, month, day, hour, minute, second, frac_second, tz_offset, tz_name = date_tup
    date = date_cls(year, month, day)
    day_of_week = date.day_of_week()
    ordinal_day = date.ordinal_date()
    iso_date = IsoWeekDate(date)
    
    return cls.format_string_from_info({
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
      'tz_name': tz_name,
      'iso_week_date_year': iso_date.year,
      'iso_week_date_week': iso_date.week,
      'iso_week_date_day': iso_date.day,
    }, format_str, date_cls = date_cls)
  
  def to_format_string_tai(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a TAI time string formatted in the strftime style.'
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_tai(date_cls = date_cls),
        tz_offset = -self.get_utc_tai_offset(),
        tz_name = 'Time Atomic International'
      )
    )
  
  def to_format_string_utc(self, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a UTC time string formatted in the strftime style.'
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_utc(date_cls = date_cls),
        tz_offset = 0,
        tz_name = 'Universal Time Coordinated'
      )
    )
  
  def to_format_string_tz(self, time_zone: TimeZone, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a timezone time string formatted in the strftime style.'
    
    tz_offset, tz_offset_abbr = self.get_current_tz_offset(time_zone, date_cls = date_cls)
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_tz(time_zone, date_cls = date_cls)[:7],
        tz_offset = tz_offset,
        tz_name = tz_offset_abbr
      )
    )
  
  def to_format_string_mono(self, time_scale: TimeInstantSolar.TIME_SCALES, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a monotonic-time-scale time string formatted in the strftime style.'
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_mono(time_scale, date_cls = date_cls),
        tz_offset = -self.get_utc_tai_offset() + self.get_mono_tai_offset(time_scale),
        tz_name = time_scale.name
      )
    )
  
  def to_format_string_solar(self, longitude_deg: TimeStorageType, true_solar_time: bool, format_str: str, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a solar time string formatted in the strftime style.'
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_solar(longitude_deg, true_solar_time, date_cls = date_cls),
        tz_offset = -self.get_utc_tai_offset() + self.get_solar_tai_offset(longitude_deg, true_solar_time),
        tz_name = f'Mean Solar Time {longitude_deg}deg Longitude'
      )
    )
  
  def to_format_string_smear_utc(self, smear_plan: LeapSmearPlan, format_str: str, true_utc_offset: bool = False, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a smeared UTC time string formatted in the strftime style.'
    
    if true_utc_offset:
      tz_offset = -self.get_utc_tai_offset() + self.get_smear_utc_tai_offset(smear_plan)
    else:
      tz_offset = 0
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_smear_utc(smear_plan, date_cls = date_cls),
        tz_offset = tz_offset,
        tz_name = 'Universal Time Coordinated (Smeared)'
      )
    )
  
  def to_format_string_smear_tz(self, smear_plan: LeapSmearPlan, time_zone: TimeZone, format_str: str, true_utc_offset: bool = False, date_cls: type[JulGregBaseDate] = GregorianDate) -> str:
    'Returns a smeared UTC timezone string formatted in the strftime style.'
    
    tz_offset, tz_offset_abbr = self.get_current_tz_offset_smear(smear_plan, time_zone, true_utc_offset = true_utc_offset, date_cls = date_cls)
    
    return self.date_tuple_to_format_string(
      format_str = format_str,
      date_cls = date_cls,
      date_tup = DateTupleFormatString(
        *self.to_date_tuple_smear_tz(smear_plan, time_zone, date_cls = date_cls)[:7],
        tz_offset = tz_offset,
        tz_name = f'{self.DEFAULT_TIMEZONE_NAME if tz_offset_abbr == None else tz_offset_abbr} (Smeared)'
      )
    )
