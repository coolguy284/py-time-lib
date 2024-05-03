from .time_classes.time_instant.time_inst import TimeInstant
from .time_classes.time_zone import TimeZone
from .time_classes.lib import TimeStorageType
from .update_leap_seconds import get_leap_sec_data

from .data_py import leap_seconds as _leap_seconds
from .update_leap_seconds import DEFAULT_LOG_DOWNLOADS as _DEFAULT_LOG_DOWNLOADS
from .update_leap_seconds import DEFAULT_LEAP_FILE_PATH as _DEFAULT_LEAP_FILE_PATH
from .update_leap_seconds import DEFAULT_LEAP_FILE_URL as _DEFAULT_LEAP_FILE_URL
from .update_timezone_db import DEFAULT_TZDB_UPDATE_CHECK_TIME as _DEFAULT_TZDB_UPDATE_CHECK_TIME
from .update_timezone_db import DEFAULT_TZDB_URL as _DEFAULT_TZDB_URL
from .update_timezone_db import DEFAULT_TZDB_VERSION_URL as _DEFAULT_TZDB_VERSION_URL
from .update_timezone_db import DEFAULT_TZDB_PATH as _DEFAULT_TZDB_PATH
from .update_timezone_db import DEFAULT_TZDB_DOWNLOADED_TIME_PATH as _DEFAULT_TZDB_DOWNLOADED_TIME_PATH
from .update_timezone_db import get_tzdb_data as _Tzdb_get_tzdb_data
from .update_ut1 import DEFAULT_HISTORICAL_UPDATE_TIME as _DEFAULT_HISTORICAL_UPDATE_TIME
from .update_ut1 import DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH as _DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH
from .update_ut1 import DEFAULT_HISTORICAL_FILE_PATH as _DEFAULT_HISTORICAL_FILE_PATH
from .update_ut1 import DEFAULT_HISTORICAL_URL as _DEFAULT_HISTORICAL_URL
from .update_ut1 import DEFAULT_RECENT_UPDATE_TIME as _DEFAULT_RECENT_UPDATE_TIME
from .update_ut1 import DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH as _DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH
from .update_ut1 import DEFAULT_RECENT_FILE_PATH as _DEFAULT_RECENT_FILE_PATH
from .update_ut1 import DEFAULT_RECENT_URL as _DEFAULT_RECENT_URL
from .update_ut1 import DEFAULT_DAILY_UPDATE_TIME as _DEFAULT_DAILY_UPDATE_TIME
from .update_ut1 import DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH as _DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH
from .update_ut1 import DEFAULT_DAILY_FILE_PATH as _DEFAULT_DAILY_FILE_PATH
from .update_ut1 import DEFAULT_DAILY_URL as _DEFAULT_DAILY_URL
from .update_ut1 import get_ut1_offsets as _Ut1_get_ut1_offsets

TIMEZONES: dict[str, dict[str, TimeZone]] = {
  'proleptic_variable': {},
  'proleptic_fixed': {},
  'full_varying': {},
  'full_fixed': {},
}

def update_leap_seconds(log_downloads: bool = _DEFAULT_LOG_DOWNLOADS, file_path: str = _DEFAULT_LEAP_FILE_PATH, url: str = _DEFAULT_LEAP_FILE_URL):
  leap_sec_data = get_leap_sec_data(log_downloads = log_downloads, file_path = file_path, url = url)
  _leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI = leap_sec_data['initial_utc_tai_offset']
  _leap_seconds.LEAP_SECONDS = leap_sec_data['leap_seconds']
  TimeInstant.UTC_INITIAL_OFFSET_FROM_TAI = _leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI
  TimeInstant.LEAP_SECONDS = _leap_seconds.LEAP_SECONDS
  TimeInstant._init_class_vars()

def update_timezone_data(
    log_downloads: bool = _DEFAULT_LOG_DOWNLOADS,
    update_check_time: TimeStorageType = _DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = _DEFAULT_TZDB_URL,
    version_url: str = _DEFAULT_TZDB_VERSION_URL,
    db_file_path: str = _DEFAULT_TZDB_PATH,
    downloaded_time_file_path: str = _DEFAULT_TZDB_DOWNLOADED_TIME_PATH
  ) -> None:
  new_data = _Tzdb_get_tzdb_data(
    log_downloads = log_downloads,
    update_check_time = update_check_time,
    tzdb_url = tzdb_url,
    version_url = version_url,
    db_file_path = db_file_path,
    downloaded_time_file_path = downloaded_time_file_path
  )
  for key in new_data:
    TIMEZONES[key] = new_data[key]

def update_ut1_offsets(
    historic_min_redownload_age: TimeStorageType | None = _DEFAULT_HISTORICAL_UPDATE_TIME,
    historic_downloaded_time_file_path: str = _DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
    historic_data_file_path: str = _DEFAULT_HISTORICAL_FILE_PATH,
    historic_url: str = _DEFAULT_HISTORICAL_URL,
    recent_min_redownload_age: TimeStorageType | None = _DEFAULT_RECENT_UPDATE_TIME,
    recent_downloaded_time_file_path: str = _DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
    recent_data_file_path: str = _DEFAULT_RECENT_FILE_PATH,
    recent_url: str = _DEFAULT_RECENT_URL,
    daily_min_redownload_age: TimeStorageType | None = _DEFAULT_DAILY_UPDATE_TIME,
    daily_downloaded_time_file_path: str = _DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    daily_data_file_path: str = _DEFAULT_DAILY_FILE_PATH,
    daily_url: str = _DEFAULT_DAILY_URL
  ) -> None:
  TimeInstant.UT1_OFFSETS[:] = _Ut1_get_ut1_offsets(
    historic_min_redownload_age,
    historic_downloaded_time_file_path,
    historic_data_file_path,
    historic_url,
    recent_min_redownload_age,
    recent_downloaded_time_file_path,
    recent_data_file_path,
    recent_url,
    daily_min_redownload_age,
    daily_downloaded_time_file_path,
    daily_data_file_path,
    daily_url
  )

def update_time_databases(
    log_downloads: bool = _DEFAULT_LOG_DOWNLOADS,
    
    leapsec_file_path: str = _DEFAULT_LEAP_FILE_PATH,
    leapsec_url: str = _DEFAULT_LEAP_FILE_URL,
    
    tzdb_update_check_time: TimeStorageType | None = _DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = _DEFAULT_TZDB_URL,
    tzdb_version_url: str = _DEFAULT_TZDB_VERSION_URL,
    tzdb_file_path: str = _DEFAULT_TZDB_PATH,
    tzdb_downloaded_time_file_path: str = _DEFAULT_TZDB_DOWNLOADED_TIME_PATH,
    
    ut1_historic_min_redownload_age: TimeStorageType | None = _DEFAULT_HISTORICAL_UPDATE_TIME,
    ut1_historic_downloaded_time_file_path: str = _DEFAULT_HISTORICAL_DOWNLOADED_TIME_FILE_PATH,
    ut1_historic_data_file_path: str = _DEFAULT_HISTORICAL_FILE_PATH,
    ut1_historic_url: str = _DEFAULT_HISTORICAL_URL,
    ut1_recent_min_redownload_age: TimeStorageType | None = _DEFAULT_RECENT_UPDATE_TIME,
    ut1_recent_downloaded_time_file_path: str = _DEFAULT_RECENT_DOWNLOADED_TIME_FILE_PATH,
    ut1_recent_data_file_path: str = _DEFAULT_RECENT_FILE_PATH,
    ut1_recent_url: str = _DEFAULT_RECENT_URL,
    ut1_daily_min_redownload_age: TimeStorageType | None = _DEFAULT_DAILY_UPDATE_TIME,
    ut1_daily_downloaded_time_file_path: str = _DEFAULT_DAILY_DOWNLOADED_TIME_FILE_PATH,
    ut1_daily_data_file_path: str = _DEFAULT_DAILY_FILE_PATH,
    ut1_daily_url: str = _DEFAULT_DAILY_URL
  ) -> None:
  update_leap_seconds(
    log_downloads = log_downloads,
    file_path = leapsec_file_path,
    url = leapsec_url
  )
  update_timezone_data(
    log_downloads = log_downloads,
    update_check_time = tzdb_update_check_time,
    tzdb_url = tzdb_url,
    version_url = tzdb_version_url,
    db_file_path = tzdb_file_path,
    downloaded_time_file_path = tzdb_downloaded_time_file_path
  )
  update_ut1_offsets(
    historic_min_redownload_age = ut1_historic_min_redownload_age,
    historic_downloaded_time_file_path = ut1_historic_downloaded_time_file_path,
    historic_data_file_path = ut1_historic_data_file_path,
    historic_url = ut1_historic_url,
    recent_min_redownload_age = ut1_recent_min_redownload_age,
    recent_downloaded_time_file_path = ut1_recent_downloaded_time_file_path,
    recent_data_file_path = ut1_recent_data_file_path,
    recent_url = ut1_recent_url,
    daily_min_redownload_age = ut1_daily_min_redownload_age,
    daily_downloaded_time_file_path = ut1_daily_downloaded_time_file_path,
    daily_data_file_path = ut1_daily_data_file_path,
    daily_url = ut1_daily_url
  )
