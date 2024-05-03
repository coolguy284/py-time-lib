from re import compile as re_compile

from .lib_funcs import binary_search, file_at_path_exists, get_file_at_path, set_file_at_path, get_file_from_online
from .fixed_prec import FixedPrec
from .time_classes.lib import TimeStorageType
from .time_classes.time_instant.time_inst import TimeInstant
from .constants import NOMINAL_SECS_PER_DAY
from .named_tuples import UT1TAIOffsetEntry

DEFAULT_HISTORICAL_URL = 'https://datacenter.iers.org/data/latestVersion/EOP_C01_IAU2000_1846-now.txt'
DEFAULT_HISTORICAL_FILE_PATH = 'data/EOP_C01_IAU2000_1846-now.txt'
DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH = 'data/eop-historic-downloaded-time.txt'
DEFAULT_HISTORICAL_UPDATE_TIME = 365 * NOMINAL_SECS_PER_DAY
DEFAULT_RECENT_URL = 'https://datacenter.iers.org/data/latestVersion/finals.all.iau2000.txt'
DEFAULT_RECENT_FILE_PATH = 'data/finals.all.iau2000.txt'
DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH = 'data/eop-recent-downloaded-time.txt'
DEFAULT_RECENT_UPDATE_TIME = 30 * NOMINAL_SECS_PER_DAY
DEFAULT_DAILY_URL = 'https://datacenter.iers.org/data/latestVersion/finals.daily.iau2000.txt'
DEFAULT_DAILY_FILE_PATH = 'data/finals.daily.iau2000.txt'
DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH = 'data/eop-daily-downloaded-time.txt'
DEFAULT_DAILY_UPDATE_TIME = 1 * NOMINAL_SECS_PER_DAY

def _get_file(
    file_descriptor: str,
    min_redownload_age: TimeStorageType | None,
    downloaded_time_file_path: str,
    data_file_path: str,
    url: str
  ) -> str:
  current_instant = TimeInstant.now()
  
  create_new_file = False
  
  if file_at_path_exists(downloaded_time_file_path):
    if min_redownload_age != None:
      downloaded_time = TimeInstant(get_file_at_path(downloaded_time_file_path).decode().strip())
      file_age = current_instant - downloaded_time
      if file_age.time_delta > min_redownload_age:
        create_new_file = True
  else:
    create_new_file = True
  
  if create_new_file:
    print(f'Downloading EOP {file_descriptor} file from {url}...')
    file_contents = get_file_from_online(url)
    set_file_at_path(downloaded_time_file_path, str(current_instant.time).encode())
    set_file_at_path(data_file_path, file_contents)
  else:
    file_contents = get_file_at_path(data_file_path)
  
  return file_contents.decode()

def eop_historic_get_file(
    min_redownload_age: TimeStorageType | None = DEFAULT_HISTORICAL_UPDATE_TIME,
    downloaded_time_file_path: str = DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
    data_file_path: str = DEFAULT_HISTORICAL_FILE_PATH,
    url: str = DEFAULT_HISTORICAL_URL
  ) -> str:
  return _get_file(
    'historic',
    min_redownload_age,
    downloaded_time_file_path,
    data_file_path,
    url
  )

def eop_recent_get_file(
    min_redownload_age: TimeStorageType | None = DEFAULT_RECENT_UPDATE_TIME,
    downloaded_time_file_path: str = DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
    data_file_path: str = DEFAULT_RECENT_FILE_PATH,
    url: str = DEFAULT_RECENT_URL
  ) -> str:
  return _get_file(
    'recent',
    min_redownload_age,
    downloaded_time_file_path,
    data_file_path,
    url
  )

def eop_daily_get_file(
    min_redownload_age: TimeStorageType | None = DEFAULT_DAILY_UPDATE_TIME,
    downloaded_time_file_path: str = DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    data_file_path: str = DEFAULT_DAILY_FILE_PATH,
    url: str = DEFAULT_DAILY_URL
  ) -> str:
  return _get_file(
    'daily',
    min_redownload_age,
    downloaded_time_file_path,
    data_file_path,
    url
  )

_historic_file_line = re_compile(r'^\s*(-?\d+\.\d{3})(?:\s+(?:-?\d+\.\d{6})){2}\s+(-?\d+\.\d{7})(?:\s+(?:-?\d+\.\d{6})){4}\s+(-?\d+\.\d{7}).*$')
_recent_file_line = re_compile(r'^(?:[0-9 ]{2}){3}\s+(-?\d+\.\d{2})(?:\s+[IP](?:\s+(?:-?\d+\.\d{6})){4}(?:\s+[IP]\s{0,1}(-?\d+\.\d{7})\s+(?:\d+\.\d{7}))?)?')

def parse_historic_file(file_str: str) -> list[UT1TAIOffsetEntry]:
  file_lines = [line for line in file_str.strip().splitlines() if not line.startswith('#')]
  
  ut1_offset_list = []
  
  for line in file_lines:
    if match := _historic_file_line.match(line):
      ut1_minus_tai_error_str = match[3]
      # ignore invalid values
      if ut1_minus_tai_error_str != '99.9900000':
        mjd = FixedPrec(match[1])
        ut1_minus_tai = FixedPrec(match[2])
        
        tai_secs_since_epoch = TimeInstant.from_modified_julian_date_utc(mjd).time
        
        ut1_offset_list.append(UT1TAIOffsetEntry(tai_secs_since_epoch, ut1_minus_tai))
    else:
      raise ValueError(f'Historic file line invalid format: {line!r}')
  
  return ut1_offset_list

def parse_recent_files(file_str: str) -> list[UT1TAIOffsetEntry]:
  file_lines = file_str.strip().splitlines()
  
  ut1_offset_list = []
  
  for line in file_lines:
    if match := _recent_file_line.match(line):
      # ignore lines without information
      if match[2] != None:
        mjd = FixedPrec(match[1])
        ut1_minus_utc = FixedPrec(match[2])
        
        instant = TimeInstant.from_modified_julian_date_utc(mjd)
        
        tai_secs_since_epoch = instant.time
        ut1_minus_tai = instant.get_utc_tai_offset() + ut1_minus_utc
        
        ut1_offset_list.append(UT1TAIOffsetEntry(tai_secs_since_epoch, ut1_minus_tai))
    else:
      raise ValueError(f'Recent file line invalid format: {line!r}')
  
  return ut1_offset_list

def parse_ut1_offsets(historic_file_str: str, recent_file_str: str, daily_file_str: str) -> list[UT1TAIOffsetEntry]:
  historic_data = parse_historic_file(historic_file_str)
  recent_data = parse_recent_files(recent_file_str)
  daily_data = parse_recent_files(daily_file_str)
  
  if len(recent_data) == 0:
    raise ValueError(f'Recent data length must be greater than 0')
  
  full_data = historic_data[:]
  
  first_recent_data_secs_since_epoch = recent_data[0].secs_since_epoch
  
  recent_data_insert_index = binary_search(lambda x: full_data[x].secs_since_epoch < first_recent_data_secs_since_epoch, 0, len(full_data)) + 1
  
  full_data[recent_data_insert_index:] = recent_data
  
  if len(daily_data) > 0:
    first_daily_data_secs_since_epoch = daily_data[0].secs_since_epoch
    last_daily_data_secs_since_epoch = daily_data[-1].secs_since_epoch
    
    daily_data_start_insert_index = binary_search(lambda x: full_data[x].secs_since_epoch < first_daily_data_secs_since_epoch, 0, len(full_data)) + 1
    daily_data_end_insert_index = binary_search(lambda x: full_data[x].secs_since_epoch <= last_daily_data_secs_since_epoch, 0, len(full_data)) + 1
    
    full_data[daily_data_start_insert_index:daily_data_end_insert_index] = daily_data
  
  return full_data

def get_ut1_offsets(
    historic_min_redownload_age: TimeStorageType | None = DEFAULT_HISTORICAL_UPDATE_TIME,
    historic_downloaded_time_file_path: str = DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
    historic_data_file_path: str = DEFAULT_HISTORICAL_FILE_PATH,
    historic_url: str = DEFAULT_HISTORICAL_URL,
    recent_min_redownload_age: TimeStorageType | None = DEFAULT_RECENT_UPDATE_TIME,
    recent_downloaded_time_file_path: str = DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
    recent_data_file_path: str = DEFAULT_RECENT_FILE_PATH,
    recent_url: str = DEFAULT_RECENT_URL,
    daily_min_redownload_age: TimeStorageType | None = DEFAULT_DAILY_UPDATE_TIME,
    daily_downloaded_time_file_path: str = DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    daily_data_file_path: str = DEFAULT_DAILY_FILE_PATH,
    daily_url: str = DEFAULT_DAILY_URL
  ) -> list[UT1TAIOffsetEntry]:
  return parse_ut1_offsets(
    eop_historic_get_file(
      min_redownload_age = historic_min_redownload_age,
      downloaded_time_file_path = historic_downloaded_time_file_path,
      data_file_path = historic_data_file_path,
      url = historic_url
    ),
    eop_recent_get_file(
      min_redownload_age = recent_min_redownload_age,
      downloaded_time_file_path = recent_downloaded_time_file_path,
      data_file_path = recent_data_file_path,
      url = recent_url
    ),
    eop_daily_get_file(
      min_redownload_age = daily_min_redownload_age,
      downloaded_time_file_path = daily_downloaded_time_file_path,
      data_file_path = daily_data_file_path,
      url = daily_url
    )
  )
