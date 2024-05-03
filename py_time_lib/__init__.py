from .lib_funcs import binary_search, binary_search_float, binary_search_array_split
from .lib_funcs import fancy_format
from .lib_funcs import file_relative_path_to_abs, file_at_path_exists, get_file_at_path, set_file_at_path, get_file_from_online
from .exceptions import TimeUnmappableError
from .fixed_prec import FixedPrec
from .calendars.date_delta import DateDelta
from .calendars.date_base import DateBase
from .calendars.jul_greg_base import JulGregBaseDate
from .calendars.julian import JulianDate
from .calendars.gregorian import GregorianDate
from .calendars.iso_weekdate import IsoWeekDate
from .calendars.holocene import HoloceneDate
from .calendars.symmetry import SymmetryBase, Symmetry010, Symmetry010LeapMonth, Symmetry454, Symmetry454LeapMonth
from .time_classes.lib import TimeStorageType
from .time_classes.time_delta import TimeDelta
from .time_classes.time_instant.time_inst import TimeInstant
from .time_classes.time_zone import TimeZone
from .named_tuples import MonthWeekDate
from .named_tuples import LeapSecEntry, SecsSinceEpochUTC, SecsSinceEpochTZ, DateTupleBasic, DateTupleTZ, UnixTimestampUTC
from .update_leap_seconds import get_leap_sec_data

from .calendars.date_base import _init_module_vars as _DateBase_init_module_vars
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

_DateBase_init_module_vars()

def update_leap_seconds(log_downloads: bool = _DEFAULT_LOG_DOWNLOADS, file_path: str = _DEFAULT_LEAP_FILE_PATH, url: str = _DEFAULT_LEAP_FILE_URL):
  leap_sec_data = get_leap_sec_data(log_downloads = log_downloads, file_path = file_path, url = url)
  _leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI = leap_sec_data['initial_utc_tai_offset']
  _leap_seconds.LEAP_SECONDS = leap_sec_data['leap_seconds']
  TimeInstant.UTC_INITIAL_OFFSET_FROM_TAI = _leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI
  TimeInstant.LEAP_SECONDS = _leap_seconds.LEAP_SECONDS
  TimeInstant._init_class_vars()

TIMEZONES: dict[str, dict[str, TimeZone]] = {
  'proleptic_variable': {},
  'proleptic_fixed': {},
  'full_varying': {},
  'full_fixed': {},
}

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

def update_time_databases(
    log_downloads: bool = _DEFAULT_LOG_DOWNLOADS,
    
    leapsec_file_path: str = _DEFAULT_LEAP_FILE_PATH,
    leapsec_url: str = _DEFAULT_LEAP_FILE_URL,
    
    tzdb_update_check_time: TimeStorageType | None = _DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = _DEFAULT_TZDB_URL,
    tzdb_version_url: str = _DEFAULT_TZDB_VERSION_URL,
    tzdb_file_path: str = _DEFAULT_TZDB_PATH,
    tzdb_downloaded_time_file_path: str = _DEFAULT_TZDB_DOWNLOADED_TIME_PATH
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
