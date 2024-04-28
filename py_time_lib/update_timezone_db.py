from contextlib import contextmanager
from enum import Enum
from numbers import Integral
from re import compile as re_compile
from tarfile import open as tarfile_open, TarFile
from typing import Generator

from .lib_funcs import file_relative_path_to_abs, file_at_path_exists, get_file_at_path, set_file_at_path, get_file_from_online
from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate
from .time_classes.lib import TimeStorageType
from .time_classes.time_instant import time_inst
from .time_classes.time_zone import TimeZone
from .constants import NOMINAL_SECS_PER_DAY, NOMINAL_SECS_PER_MIN, NOMINAL_MINS_PER_HOUR, NOMINAL_SECS_PER_HOUR

DEFAULT_TZDB_PATH = 'data/tzdata-latest.tar.gz'
DEFAULT_TZDB_DOWNLOADED_TIME_PATH = 'data/tzdb-downloaded-time.txt'
DEFAULT_TZDB_URL = 'https://data.iana.org/time-zones/tzdata-latest.tar.gz'
DEFAULT_TZDB_VERSION_URL = 'https://data.iana.org/time-zones/tzdb/version'
DEFAULT_TZDB_UPDATE_CHECK_TIME = 90 * NOMINAL_SECS_PER_DAY

def tzdb_stored_file_exists(file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH) -> bool:
  return file_at_path_exists(file_path)

def get_tzdb_stored_file_downloaded_time(file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH) -> time_inst.TimeInstant:
  return time_inst.TimeInstant(get_file_at_path(file_path).decode().strip())

@contextmanager
def get_tzdb_stored_file(file_path: str = DEFAULT_TZDB_PATH) -> Generator[TarFile, None, None]:
  with tarfile_open(file_relative_path_to_abs(file_path)) as tgz_file:
    yield tgz_file

def set_tzdb_stored_file_downloaded_time(time: time_inst.TimeInstant, file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH) -> None:
  set_file_at_path(file_path, f'{time.time!s}\n'.encode())

def set_tzdb_stored_file(contents: bytes, file_path: str = DEFAULT_TZDB_PATH) -> None:
  set_file_at_path(file_path, contents)

def get_tzdb_online_file(url: str = DEFAULT_TZDB_URL) -> bytes:
  print('of')
  return get_file_from_online(url)

def get_tzdb_online_version(url: str = DEFAULT_TZDB_VERSION_URL) -> str:
  print('ofv')
  return get_file_from_online(url).decode().strip()

def parse_tzdb_version(tgz_file: TarFile) -> str:
  with tgz_file.extractfile('version') as f:
    return f.read().decode().strip()

_parse_tzdb_omitted_files = set(('version', 'calendars', 'Makefile', 'leap-seconds.list'))
_parse_tzdb_unused_files = set(('factory', 'leapseconds'))

_parse_tzdb_line_comment_regex = re_compile(r'^([^#]*)(?:#.*)?$')
_parse_tzdb_line_split_regex = re_compile(r'\s+')

_parse_tzdb_week_names_regex_part = '|'.join(GregorianDate.WEEK_NAMES_SHORT)
_parse_tzdb_rule_date_int_regex = re_compile(r'^(\d+)$')
_parse_tzdb_rule_date_last_regex = re_compile(r'^last(' + _parse_tzdb_week_names_regex_part + r')$')
_parse_tzdb_rule_date_ge_regex = re_compile(r'^(' + _parse_tzdb_week_names_regex_part + r')>=(\d+)$')
_parse_tzdb_rule_date_le_regex = re_compile(r'^(' + _parse_tzdb_week_names_regex_part + r')<=(\d+)$')

_parse_tzdb_time_regex = re_compile(r'^(\d{1,2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(|[sguzw])$')
_parse_tzdb_time_types = Enum('_parse_tzdb_rule_time_types', (
  'WALL',
  'STANDARD',
  'UTC',
))
_parse_tzdb_offset_regex = re_compile(r'^(?:(-?)(\d+)(?::(\d{2})(?::(\d{2})(?:\.(\d+))?)?)?)$')
type _parse_tzdb_DayDict = dict[str, TimeZone.OffsetDayMode | int | bool]

def _parse_tzdb_time_str_to_fixedprec_secs_from_day_start(time_str: str) -> tuple[FixedPrec, _parse_tzdb_time_types]:
  if match := _parse_tzdb_time_regex.match(time_str):
    secs_since_day_start = FixedPrec(match[1]) * NOMINAL_SECS_PER_HOUR
    secs_since_day_start += FixedPrec(match[2]) * NOMINAL_SECS_PER_MIN
    if match[3] != None:
      secs_since_day_start += FixedPrec(match[3])
      if match[4] != None:
        secs_since_day_start += FixedPrec(f'0.{match[4]}')
    
    if match[5] == '' or match[5] == 'w':
      time_mode = _parse_tzdb_time_types.WALL
    elif match[5] == 's':
      time_mode = _parse_tzdb_time_types.STANDARD
    else:
      time_mode = _parse_tzdb_time_types.UTC
    
    return secs_since_day_start, time_mode
  else:
    raise ValueError(f'Time string format unknown: {time_str}')

def _parse_tzdb_offset_str_to_fixedprec_secs(offset_str: str) -> FixedPrec:
  if match := _parse_tzdb_offset_regex.match(offset_str):
    offset_abs = FixedPrec(match[2]) * NOMINAL_SECS_PER_HOUR
    if match[3] != None:
      offset_abs += FixedPrec(match[3]) * NOMINAL_SECS_PER_MIN
      if match[4] != None:
        offset_abs += FixedPrec(match[4])
        if match[5] != None:
          offset_abs += FixedPrec('0.' + match[5])
    
    sign = -1 if match[1] == '-' else 1
    
    return offset_abs * sign
  else:
    raise ValueError(f'Offset string format unknown: {offset_str}')

def _parse_tzdb_parse_day_in_month_str(day_in_month_str: str) -> _parse_tzdb_DayDict:
  if match := _parse_tzdb_rule_date_int_regex.match(day_in_month_str):
    return {
      'offset_day_mode': TimeZone.OffsetDayMode.MONTH_AND_DAY,
      'day': int(match[1]),
    }
  elif match := _parse_tzdb_rule_date_last_regex.match(day_in_month_str):
    return {
      'offset_day_mode': TimeZone.OffsetDayMode.MONTH_WEEK_DAY,
      'week': 1,
      'day_in_week': GregorianDate.WEEK_NAMES_SHORT.index(match[1]),
      'from_month_end': True,
    }
  elif match := _parse_tzdb_rule_date_ge_regex.match(day_in_month_str):
    return {
      'offset_day_mode': TimeZone.OffsetDayMode.MONTH_WEEKDAY_DAY_GE,
      'day_in_week': GregorianDate.WEEK_NAMES_SHORT.index(match[1]),
      'day': int(match[2]),
    }
  elif match := _parse_tzdb_rule_date_le_regex.match(day_in_month_str):
    return {
      'offset_day_mode': TimeZone.OffsetDayMode.MONTH_WEEKDAY_DAY_LE,
      'day_in_week': GregorianDate.WEEK_NAMES_SHORT.index(match[1]),
      'day': int(match[2]),
    }
  else:
    raise ValueError(f'day in month format unknown: {day_in_month_str}')

def _parse_tzdb_day_in_month_dict_to_date(year: Integral, month: Integral, day_dict: _parse_tzdb_DayDict) -> GregorianDate:
  return TimeZone.realize_offset_entry(year, {
    'month': month,
    **day_dict,
  })

def _parse_tzdb_get_filtered_lines(tgz_file: TarFile) -> list[str]:
  # get all zone/rule files
  
  all_names = tgz_file.getnames()
  
  zone_names = [
    name
    for name in all_names
    if
      name not in _parse_tzdb_omitted_files and
      not name.isupper() and
      not name.endswith('.html') and
      not name.endswith('.awk') and
      not name.endswith('.tab')
  ]
  
  used_zone_names = [
    name
    for name in zone_names
    if name not in _parse_tzdb_unused_files
  ]
  
  # get all zone/rule lines
  
  all_lines = []
  
  for filename in used_zone_names:
    with tgz_file.extractfile(filename) as f:
      lines = f.read().decode().split('\n')
      all_lines.extend(lines)
  
  # filter out comments
  
  filtered_lines = []
  
  for line in all_lines:
    match = _parse_tzdb_line_comment_regex.match(line)
    
    non_comment = match[1]
    
    if len(non_comment.strip()) > 0:
      filtered_lines.append(non_comment)
  
  return filtered_lines

def _parse_tzdb_get_processed_lines(filtered_lines: list[str]) -> list[list[str]]:
  # split lines to each part
  
  lines_split = []
  
  for line in filtered_lines:
    line_split = _parse_tzdb_line_split_regex.split(line)
    
    if line_split[0] == '':
      line_split = (('Zone-Continue',), *(part for part in line_split))
    
    line_split = tuple(part for part in line_split if len(part) > 0)
    
    lines_split.append(line_split)
  
  return lines_split

def _parse_tzdb_get_result_dicts_zone(offset_str, rules, abbr_format, until_list):
  entry_dict = {}
  
  entry_dict['utc_offset'] = _parse_tzdb_offset_str_to_fixedprec_secs(offset_str)
  entry_dict['rule'] = None if rules == '-' else rules
  entry_dict['abbreviation_format'] = abbr_format
  
  if len(until_list) == 0:
    entry_dict['until'] = None
  elif len(until_list) <= 5:
    year = int(until_list[0])
    
    if len(until_list) >= 2:
      month = GregorianDate.MONTH_NAMES_SHORT.index(until_list[1]) + 1
      
      if len(until_list) >= 3:
        day_dict = _parse_tzdb_parse_day_in_month_str(until_list[2])
        
        if len(until_list) >= 4:
          secs_since_day_start, time_mode = _parse_tzdb_time_str_to_fixedprec_secs_from_day_start(until_list[3])
        else:
          secs_since_day_start = FixedPrec(0)
          time_mode = _parse_tzdb_time_types.WALL
      else:
        day_dict = {
          'offset_day_mode': TimeZone.OffsetDayMode.MONTH_AND_DAY,
          'day': 1,
        }
        secs_since_day_start = FixedPrec(0)
        time_mode = _parse_tzdb_time_types.WALL
    else:
      month = 1
      day_dict = {
        'offset_day_mode': TimeZone.OffsetDayMode.MONTH_AND_DAY,
        'day': 1,
      }
      secs_since_day_start = FixedPrec(0)
      time_mode = _parse_tzdb_time_types.WALL
    
    time_since_year_start = (
      _parse_tzdb_day_in_month_dict_to_date(year, month, day_dict) -
      GregorianDate(year, 1, 1)
    ).date_delta * NOMINAL_SECS_PER_DAY + secs_since_day_start
    
    entry_dict['until'] = {
      'year': year,
      'time_since_year_start': time_since_year_start,
      'time_mode': time_mode,
    }
  else:
    raise ValueError(f'Zone until format unknown: {until_list}')
  
  return entry_dict

def _parse_tzdb_get_result_dicts(lines_split: list[list[str]]) -> dict[str, dict[str, list[str | dict]]]:
  last_line_type = None
  
  # format:
  # {
  #   <rule_name: str>: [
  #     {
  #       'from_year_inclusive': int,
  #       'to_year_inclusive': int | None,
  #       'month': int (1-12),
  #       'day': {
  #         'offset_day_mode': TimeZone.OffsetDayMode,
  #         if MONTH_AND_DAY:
  #           'day': int (1-31),
  #         elif MONTH_WEEK_DAY:
  #           'week': int (1),
  #           'day_in_week': int (0-6),
  #           'from_month_end': bool (True),
  #         elif MONTH_WEEKDAY_DAY_GE:
  #           'day_in_week': int (0-6),
  #           'day': int (1-31),
  #         elif MONTH_WEEKDAY_DAY_LE:
  #           'day_in_week': int (0-6),
  #           'day': int (1-31),
  #       },
  #       'from_day_start': (FixedPrec seconds [0, 86400), _parse_tzdb_time_types (wall, standard, utc)),
  #       'offset_from_standard': FixedPrec seconds,
  #       'tz_added_letter': str (length 0 or 1),
  #     },
  #     ...
  #   ]
  #   ...
  # }
  rules_dict = {}
  
  # format:
  # {
  #   <zone_name: str>: [
  #     {
  #       'utc_offset': FixedPrec seconds,
  #       'rule': str rule name | None,
  #       'abbreviation_format': str,
  #       'until': None | {
  #         'year': int,
  #         'time_since_year_start': FixedPrec seconds,
  #       },
  #     },
  #     ...
  #   ]
  #   ...
  # }
  zones_dict = {}
  
  # format:
  # {
  #   <target_tz_name: str>: [
  #     str link name,
  #     ...
  #   ],
  #   ...
  # }
  links_dict = {}
  
  for line_split in lines_split:
    match line_split:
      case 'Rule', rule_name, from_year_str, to_year_str, _, month, date, time_str, offset_str, letter:
        last_line_type = 'Rule'
        
        entry_dict = {}
        
        entry_dict['from_year_inclusive'] = int(from_year_str)
        
        if to_year_str == 'only':
          entry_dict['to_year_inclusive'] = entry_dict['from_year_inclusive']
        elif to_year_str == 'max':
          entry_dict['to_year_inclusive'] = None
        else:
          entry_dict['to_year_inclusive'] = int(to_year_str)
        
        entry_dict['month'] = GregorianDate.MONTH_NAMES_SHORT.index(month) + 1
        entry_dict['day'] = _parse_tzdb_parse_day_in_month_str(date)
        
        entry_dict['from_day_start'] = _parse_tzdb_time_str_to_fixedprec_secs_from_day_start(time_str)
        entry_dict['offset_from_standard'] = _parse_tzdb_offset_str_to_fixedprec_secs(offset_str)
        entry_dict['tz_added_letter'] = '' if letter == '-' else letter
        
        if rule_name not in rules_dict:
          rules_dict[rule_name] = [entry_dict]
        else:
          rules_dict[rule_name].append(entry_dict)
      
      case 'Zone', zone_name, offset_str, rules, abbr_format, *until_list:
        last_line_type = 'Zone'
        
        entry_dict = _parse_tzdb_get_result_dicts_zone(offset_str, rules, abbr_format, until_list)
        
        if zone_name not in zones_dict:
          zones_dict[zone_name] = [entry_dict]
        else:
          zones_dict[zone_name].append(entry_dict)
      
      case ('Zone-Continue',), offset_str, rules, abbr_format, *until_list:
        if last_line_type == 'Zone':
          entry_dict = _parse_tzdb_get_result_dicts_zone(offset_str, rules, abbr_format, until_list)
          
          if zone_name not in zones_dict:
            zones_dict[zone_name] = [entry_dict]
          else:
            zones_dict[zone_name].append(entry_dict)
        else:
          raise ValueError(f'Cannot continue a line of type {last_line_type} {data}')
      
      case 'Link', target, link_name:
        last_line_type = 'Link'
        
        if target not in links_dict:
          links_dict[target] = [link_name]
        else:
          links_dict[target].append(link_name)
      
      case name, *data:
        raise ValueError(f'Unknown line type {name} with data {data}')
  
  return {
    'rules': rules_dict,
    'zones': zones_dict,
    'links': links_dict,
  }

def _parse_tzdb_get_tz_dicts(result_dicts: dict[str, dict[str, list[str | dict]]]) -> dict:
  # get rules and zones that go to max time
  
  rules_proleptic = {}
  
  for rule_name in result_dicts['rules']:
    rule_proleptic = sorted(list(filter(lambda x: x['to_year_inclusive'] == None, result_dicts['rules'][rule_name])), key = lambda x: x['month'])
    
    if len(rule_proleptic) > 0:
      rules_proleptic[rule_name] = rule_proleptic
  
  zones_proleptic = {}
  
  for zone_name in result_dicts['zones']:
    zone_proleptic = list(filter(lambda x: x['until'] == None, result_dicts['zones'][zone_name]))
    
    if len(zone_proleptic) > 1:
      raise ValueError(f'More than one proleptic zone rule for {zone_name}')
    elif len(zone_proleptic) == 1:
      zones_proleptic[zone_name] = zone_proleptic[0]
  
  # create timezones
  
  proleptic_varying = {}
  proleptic_fixed = {}
  
  for zone_name in zones_proleptic:
    zone_entry = zones_proleptic[zone_name]
    
    abbr_format: str = zone_entry['abbreviation_format']
    
    utc_offset = zone_entry['utc_offset']
    
    rule_name = zone_entry['rule']
    
    if rule_name in rules_proleptic:
      later_offsets = []
      
      initial_abbr = abbr_format.replace('%s', rules_proleptic[rule_name][-1]['tz_added_letter'])
      
      for rule in rules_proleptic[rule_name]:
        tz_rule = {
          **rule,
          **rule['day'],
        }
        
        from_day_start_secs, from_day_start_mode = rule['from_day_start']
        
        offset_from_standard = rule['offset_from_standard']
        
        if from_day_start_mode == _parse_tzdb_time_types.WALL:
          tz_rule['start_time_in_day'] = from_day_start_secs
        elif from_day_start_mode == _parse_tzdb_time_types.STANDARD:
          tz_rule['start_time_in_day'] = from_day_start_secs - offset_from_standard
        elif from_day_start_mode == _parse_tzdb_time_types.UTC:
          tz_rule['start_time_in_day'] = from_day_start_secs - offset_from_standard - utc_offset
        
        tz_rule['utc_offset'] = utc_offset + offset_from_standard
        
        abbr = abbr_format.replace('%s', rule['tz_added_letter'])
        tz_rule['abbreviation'] = abbr
        
        later_offsets.append(tz_rule)
        
        if abbr not in proleptic_fixed:
          proleptic_fixed[abbr] = TimeZone({
            'utc_offset': tz_rule['utc_offset'],
            'abbreviation': abbr,
          })
    else:
      initial_abbr = abbr_format
      later_offsets = ()
    
    proleptic_varying[zone_name] = TimeZone({
      'utc_offset': utc_offset,
      'abbreviation': initial_abbr,
    }, later_offsets)
    
    if initial_abbr not in proleptic_fixed:
      proleptic_fixed[initial_abbr] = TimeZone({
        'utc_offset': utc_offset,
        'abbreviation': initial_abbr,
      })
  
  # format for proleptic/full:
  # {
  #   <str: timezone name>: TimeZone,
  #   ...
  # }
  return {
    'proleptic_varying': proleptic_varying,
    'proleptic_fixed': proleptic_fixed,
    'full_varying': {},
    'full_fixed': {},
  }

def parse_tzdb(tgz_file: TarFile) -> dict:
  filtered_lines = _parse_tzdb_get_filtered_lines(tgz_file)
  lines_split = _parse_tzdb_get_processed_lines(filtered_lines)
  result_dicts = _parse_tzdb_get_result_dicts(lines_split)
  tz_dicts = _parse_tzdb_get_tz_dicts(result_dicts)
  
  return tz_dicts

def get_tzdb_stored_file_version(file_path: str = DEFAULT_TZDB_PATH) -> str:
  with get_tzdb_stored_file(file_path) as tgz_file:
    return parse_tzdb_version(tgz_file)

def update_stored_tzdb_if_needed(
    update_check_time: TimeStorageType = DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = DEFAULT_TZDB_URL,
    version_url: str = DEFAULT_TZDB_VERSION_URL,
    db_file_path: str = DEFAULT_TZDB_PATH,
    downloaded_time_file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH
  ):
  current_instant = time_inst.TimeInstant.now()
  
  create_new_file = False
  
  if not tzdb_stored_file_exists(downloaded_time_file_path):
    # no stored file
    create_new_file = True
  else:
    file_age = current_instant - get_tzdb_stored_file_downloaded_time(downloaded_time_file_path)
    if file_age.time_delta > update_check_time:
      # stored file is old enough to check for update
      file_version = get_tzdb_stored_file_version(db_file_path)
      online_version = get_tzdb_online_version(version_url)
      if online_version != file_version:
        # stored file is old
        create_new_file = True
      else:
        # stored file is new, reset version string
        set_tzdb_stored_file_downloaded_time(current_instant, downloaded_time_file_path)
    else:
      # stored file is recent enough to keep
      pass
  
  if create_new_file:
    set_tzdb_stored_file(get_tzdb_online_file(tzdb_url), db_file_path)
    set_tzdb_stored_file_downloaded_time(current_instant, downloaded_time_file_path)

def get_tzdb_data(
    update_check_time: TimeStorageType = DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = DEFAULT_TZDB_URL,
    version_url: str = DEFAULT_TZDB_VERSION_URL,
    db_file_path: str = DEFAULT_TZDB_PATH,
    downloaded_time_file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH
  ):
  'Gets timezone database from file (if not too old) or from https://data.iana.org/time-zones/tzdata-latest.tar.gz.'
  
  update_stored_tzdb_if_needed(
    update_check_time = update_check_time,
    tzdb_url = tzdb_url,
    version_url = version_url,
    db_file_path = db_file_path,
    downloaded_time_file_path = downloaded_time_file_path
  )
  
  with get_tzdb_stored_file(db_file_path) as tgz_file:
    return parse_tzdb(tgz_file)
