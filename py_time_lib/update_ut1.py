from .lib_funcs import file_at_path_exists, get_file_at_path, set_file_at_path, get_file_from_online
from .time_classes.lib import TimeStorageType
from .time_classes.time_instant import time_inst
from .constants import NOMINAL_SECS_PER_DAY
from .named_tuples import UT1OffsetEntry

DEFAULT_HISTORICAL_URL = 'https://datacenter.iers.org/data/latestVersion/EOP_C01_IAU2000_1846-now.txt'
DEFAULT_HISTORICAL_FILE_PATH = 'data/EOP_C01_IAU2000_1846-now.txt'
DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH = 'data/eop-historic-downloaded-time.txt'
DEFAULT_HISTORICAL_UPDATE_CHECK_TIME = None
DEFAULT_RECENT_URL = 'https://datacenter.iers.org/data/latestVersion/finals.all.iau2000.txt'
DEFAULT_RECENT_FILE_PATH = 'data/finals.all.iau2000.txt'
DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH = 'data/eop-recent-downloaded-time.txt'
DEFAULT_RECENT_UPDATE_CHECK_TIME = 30 * NOMINAL_SECS_PER_DAY
DEFAULT_DAILY_URL = 'https://datacenter.iers.org/data/latestVersion/finals.daily.iau2000.txt'
DEFAULT_DAILY_FILE_PATH = 'data/finals.daily.iau2000.txt'
DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH = 'data/eop-daily-downloaded-time.txt'
DEFAULT_DAILY_UPDATE_CHECK_TIME = 1 * NOMINAL_SECS_PER_DAY

def _get_file(
    file_descriptor: str,
    min_redownload_age: TimeStorageType | None,
    downloaded_time_file_path: str,
    data_file_path: str,
    url: str
  ) -> str:
  current_instant = time_inst.TimeInstant.now()
  
  create_new_file = False
  
  if file_at_path_exists(downloaded_time_file_path):
    if min_redownload_age != None:
      downloaded_time = time_inst.TimeInstant(get_file_at_path(downloaded_time_file_path).decode().strip())
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
    min_redownload_age: TimeStorageType | None = DEFAULT_HISTORICAL_UPDATE_CHECK_TIME,
    downloaded_time_file_path: str = DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
    data_file_path: str = DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
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
    min_redownload_age: TimeStorageType | None = DEFAULT_RECENT_UPDATE_CHECK_TIME,
    downloaded_time_file_path: str = DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
    data_file_path: str = DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
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
    min_redownload_age: TimeStorageType | None = DEFAULT_DAILY_UPDATE_CHECK_TIME,
    downloaded_time_file_path: str = DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    data_file_path: str = DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    url: str = DEFAULT_DAILY_URL
  ) -> str:
  return _get_file(
    'daily',
    min_redownload_age,
    downloaded_time_file_path,
    data_file_path,
    url
  )

def parse_ut1_offsets(historic_file_str: str, recent_file_str: str, daily_file_str: str) -> list[UT1OffsetEntry]:
  ...

def get_ut1_offsets(
    historic_min_redownload_age: TimeStorageType | None = DEFAULT_HISTORICAL_UPDATE_CHECK_TIME,
    historic_downloaded_time_file_path: str = DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
    historic_data_file_path: str = DEFAULT_HISTORICAL_FILE_PATH,
    historic_url: str = DEFAULT_HISTORICAL_URL,
    recent_min_redownload_age: TimeStorageType | None = DEFAULT_RECENT_UPDATE_CHECK_TIME,
    recent_downloaded_time_file_path: str = DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
    recent_data_file_path: str = DEFAULT_RECENT_FILE_PATH,
    recent_url: str = DEFAULT_RECENT_URL,
    daily_min_redownload_age: TimeStorageType | None = DEFAULT_DAILY_UPDATE_CHECK_TIME,
    daily_downloaded_time_file_path: str = DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    daily_data_file_path: str = DEFAULT_DAILY_FILE_PATH,
    daily_url: str = DEFAULT_DAILY_URL
  ) -> list[UT1OffsetEntry]:
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
