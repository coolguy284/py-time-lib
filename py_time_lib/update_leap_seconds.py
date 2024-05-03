from re import compile as re_compile

from .named_tuples import LeapSecEntry
from .lib_funcs import get_file_at_path, set_file_at_path, get_file_from_online
from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate
from .constants import NOMINAL_SECS_PER_DAY
from .time_classes.time_instant.time_inst import TimeInstant

DEFAULT_LOG_DOWNLOADS = True
DEFAULT_LEAP_FILE_PATH = 'data/leap-seconds.list'
DEFAULT_LEAP_FILE_URL = 'https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list'

def ntp_timestamp_to_days_and_secs(ntp: int) -> tuple[int, int]:
  days, seconds = divmod(ntp, NOMINAL_SECS_PER_DAY)
  return GregorianDate(1900, 1, 1).to_days_since_epoch() + days, seconds

_ntp_epoch_instant = None

def get_current_ntp_timestamp() -> int:
  global _ntp_epoch_instant
  
  if _ntp_epoch_instant == None:
    _ntp_epoch_instant = TimeInstant.from_date_tuple_utc(1900, 1, 1, 0, 0, 0, 0).to_secs_since_epoch_utc()[0]
  
  return int(TimeInstant.now().to_secs_since_epoch_utc()[0] - _ntp_epoch_instant)

def get_leap_sec_stored_file(file_path: str = DEFAULT_LEAP_FILE_PATH) -> str | None:
  result = get_file_at_path(file_path)
  
  if result != None:
    return result.decode()
  else:
    return None

def set_leap_sec_stored_file(contents: str, file_path: str = DEFAULT_LEAP_FILE_PATH) -> None:
  set_file_at_path(file_path, contents.encode())

def get_leap_sec_online_file(log_downloads: bool = DEFAULT_LOG_DOWNLOADS, url: str = DEFAULT_LEAP_FILE_URL) -> str:
  if log_downloads:
    print(f'Downloading leap second database from {url}...')
  return get_file_from_online(url).decode()

_leap_sec_file_metadata_lines = {'#$', '#@'}
_leap_sec_file_last_update_regex = re_compile(r'^#\$\s+(\d+)$')
_leap_sec_file_expiry_regex = re_compile(r'^#@\s+(\d+)$')
_leap_sec_file_leap_sec_regex = re_compile(r'^(\d+)\s+(\d+)')

def parse_leap_sec_file(file_content: str) -> dict[str, int | FixedPrec | list[LeapSecEntry]]:
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
    leap_secs.append(LeapSecEntry(GregorianDate(days_since_epoch).to_iso_string(), FixedPrec(secs), FixedPrec(leap_sec_delta)))
    past_utc_tai_offset = utc_tai_offset
  
  return {
    'last_update': last_update_timestamp,
    'expiry': expiry_timestamp,
    'initial_utc_tai_offset': FixedPrec(orig_utc_tai_offset),
    'leap_seconds': leap_secs,
  }

def get_leap_sec_data(log_downloads: bool = DEFAULT_LOG_DOWNLOADS, file_path: str = DEFAULT_LEAP_FILE_PATH, url: str = DEFAULT_LEAP_FILE_URL) -> dict[str, int | FixedPrec | list[LeapSecEntry]]:
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
    leap_secs_file_str = get_leap_sec_online_file(log_downloads = log_downloads, url = url)
    set_leap_sec_stored_file(leap_secs_file_str, file_path = file_path)
    leap_secs_data = parse_leap_sec_file(leap_secs_file_str)
  
  return leap_secs_data
