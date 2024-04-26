from contextlib import contextmanager
from re import compile as re_compile
from tarfile import open as tarfile_open, TarFile
from typing import Generator

from .lib_funcs import file_relative_path_to_abs, file_at_path_exists, get_file_at_path, set_file_at_path, get_file_from_online
from .time_classes.time_instant import time_inst
from .time_classes.lib import TimeStorageType
from .constants import NOMINAL_SECS_PER_DAY

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

def _parse_tzdb_get_processed_lines(tgz_file: TarFile) -> list[list[str]]:
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
  
  # split lines to each part
  
  lines_split = []
  
  for line in filtered_lines:
    line_split = _parse_tzdb_line_split_regex.split(line)
    
    if line_split[0] == '':
      line_split = (('Zone-Continue',), *(part for part in line_split))
    
    line_split = tuple(part for part in line_split if len(part) > 0)
    
    lines_split.append(line_split)
  
  return lines_split

def _parse_tzdb_get_result_dicts(lines_split: list[list[str]]) -> dict:
  last_line_type = None
  
  rules_dict = {}
  
  for line_split in lines_split:
    match line_split:
      case 'Rule', rule_name, from_year_str, to_year_str, _, month, date, time_str, offset_str, letter:
        last_line_type = 'Rule'
        
        entry_dict = {}
        
        entry_dict['from_year_inclusive'] = int(from_year_str)
        
        if to_year_str == 'only':
          entry_dict['to_year_inclusive'] = entry_dict['from_year_inclusive']
        
        if rule_name not in rules_dict:
          rules_dict[rule_name] = [entry_dict]
        else:
          rules_dict[rule_name].append(entry_dict)
      case 'Zone', zone_name, offset_str, rules, abbr_format, *until_tuple:
        last_line_type = 'Zone'
        ...
      case 'Link', target, link_name:
        last_line_type = 'Link'
        ...
      case ('Zone-Continue',), offset_str, rules, abbr_format, *until_tuple:
        if last_line_type == 'Zone':
          ...
        else:
          raise ValueError(f'Cannot continue a line of type {last_line_type} {data}')
      case name, *data:
        raise ValueError(f'Unknown line type {name} with data {data}')
  
  return {
    'rules': rules_dict,
  }

def parse_tzdb(tgz_file: TarFile) -> dict:
  lines_split = _parse_tzdb_get_processed_lines(tgz_file)
  
  result_dicts = _parse_tzdb_get_result_dicts(lines_split)
  
  return result_dicts

def get_tzdb_stored_file_version(file_path: str = DEFAULT_TZDB_PATH) -> str:
  with get_tzdb_stored_file(file_path) as tgz_file:
    return parse_tzdb_version(tgz_file)

def get_tzdb_data(
    update_check_time: TimeStorageType = DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = DEFAULT_TZDB_URL,
    version_url: str = DEFAULT_TZDB_VERSION_URL,
    db_file_path: str = DEFAULT_TZDB_PATH,
    downloaded_time_file_path: str = DEFAULT_TZDB_DOWNLOADED_TIME_PATH
  ):
  'Gets leap second array from file (if not too old) or from https://data.iana.org/time-zones/tzdata-latest.tar.gz.'
  
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
  
  with get_tzdb_stored_file(db_file_path) as tgz_file:
    return parse_tzdb(tgz_file)
