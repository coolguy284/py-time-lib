from pathlib import PurePath
import re
import urllib.request

from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate
from .constants import NOMINAL_SECS_PER_DAY
from .time_classes.time_instant import time_inst

DEFAULT_LEAP_FILE_PATH = 'data/leap-seconds.list'
DEFAULT_LEAP_FILE_URL = 'https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list'

def file_relative_path_to_abs(file_path: str) -> str:
  # https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory/3430395#3430395
  return PurePath(__file__).parent / file_path

def ntp_timestamp_to_days_and_secs(ntp: int) -> tuple[int, int]:
  days, seconds = divmod(ntp, NOMINAL_SECS_PER_DAY)
  return GregorianDate(1900, 1, 1).to_days_since_epoch() + days, seconds

_ntp_epoch_instant = None

def get_current_ntp_timestamp() -> int:
  global _ntp_epoch_instant
  
  if _ntp_epoch_instant == None:
    _ntp_epoch_instant = time_inst.TimeInstant.from_date_tuple_utc(1900, 1, 1, 0, 0, 0, 0).to_utc_secs_since_epoch()[0]
  
  return int(time_inst.TimeInstant.now().to_utc_secs_since_epoch()[0] - _ntp_epoch_instant)

def get_leap_sec_stored_file(file_path: str = DEFAULT_LEAP_FILE_PATH) -> str | None:
  try:
    with open(file_relative_path_to_abs(file_path)) as f:
      return f.read()
  except FileNotFoundError:
    return None

def set_leap_sec_stored_file(contents, file_path: str = DEFAULT_LEAP_FILE_PATH):
  with open(file_relative_path_to_abs(file_path), 'w') as f:
    f.write(contents)

def get_leap_sec_online_file(url: str = DEFAULT_LEAP_FILE_URL) -> str:
  response = urllib.request.urlopen(url)
  
  if response.status != 200:
    raise RuntimeError('Leap second request failed')
  
  return response.read().decode()

_leap_sec_file_metadata_lines = {'#$', '#@'}
_leap_sec_file_last_update_regex = re.compile(r'^#\$\s+(\d+)$')
_leap_sec_file_expiry_regex = re.compile(r'^#@\s+(\d+)$')
_leap_sec_file_leap_sec_regex = re.compile(r'^(\d+)\s+(\d+)')

def parse_leap_sec_file(file_content: str) -> dict[str, int | FixedPrec | list[tuple[str, FixedPrec, FixedPrec]]]:
  file_lines = file_content.split('\n')
  
  # strip comments
  file_lines = [line for line in file_lines if len(line) > 0 and (line[:2] in _leap_sec_file_metadata_lines or line[:1] != '#')]
  
  last_update_line = None
  expiry_line = None
  leap_sec_lines = []
  
  for line in file_lines:
    if line[:1] != '#':
      leap_sec_lines.append(line)
    elif line[:2] == '#$':
      last_update_line = line
    else:
      expiry_line = line
  
  last_update_timestamp = int(_leap_sec_file_last_update_regex.match(last_update_line)[1])
  expiry_timestamp = int(_leap_sec_file_expiry_regex.match(expiry_line)[1])
  leap_secs_raw = []
  for line in leap_sec_lines:
    match = _leap_sec_file_leap_sec_regex.match(line)
    timestamp_str = match[1]
    offset_str = match[2]
    leap_secs_raw.append((int(timestamp_str), int(offset_str)))
  
  leap_secs = []
  
  orig_utc_tai_offset = -leap_secs_raw[0][1]
  past_utc_tai_offset = orig_utc_tai_offset
  
  for leap_time, new_utc_tai_offset in leap_secs_raw[1:]:
    days_since_epoch, secs = ntp_timestamp_to_days_and_secs(leap_time)
    utc_tai_offset = -new_utc_tai_offset
    leap_sec_delta = utc_tai_offset - past_utc_tai_offset
    leap_secs.append((GregorianDate(days_since_epoch).to_iso_string(), FixedPrec(secs), FixedPrec(leap_sec_delta)))
    past_utc_tai_offset = utc_tai_offset
  
  return {
    'last_update': last_update_timestamp,
    'expiry': expiry_timestamp,
    'initial_utc_tai_offset': FixedPrec(orig_utc_tai_offset),
    'leap_seconds': leap_secs,
  }

def get_leap_sec_data(file_path = DEFAULT_LEAP_FILE_PATH, url = DEFAULT_LEAP_FILE_URL) -> dict[str, int | FixedPrec | list[tuple[str, FixedPrec, FixedPrec]]]:
  'Gets leap second array from file (if not past expiry) or from https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list.'
  
  current_timestamp = get_current_ntp_timestamp()
  
  leap_secs_file_str = get_leap_sec_stored_file(file_path)
  
  create_new_file = False
  
  if leap_secs_file_str == None:
    # no stored file in the first place
    create_new_file = True
  else:
    leap_secs_data = parse_leap_sec_file(leap_secs_file_str)
    if current_timestamp > leap_secs_data['expiry']:
      # stored file is past expiry, replace it with new file
      create_new_file = True
  
  if create_new_file:
    leap_secs_file_str = get_leap_sec_online_file(url = url)
    set_leap_sec_stored_file(leap_secs_file_str, file_path = file_path)
    leap_secs_data = parse_leap_sec_file(leap_secs_file_str)
  
  return leap_secs_data
