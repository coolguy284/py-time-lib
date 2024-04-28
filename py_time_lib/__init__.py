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
from .time_classes.lib import TimeStorageType
from .time_classes.time_delta import TimeDelta
from .time_classes.time_instant.time_inst import TimeInstant
from .time_classes.time_zone import TimeZone
from .named_tuples import MonthWeekDate
from .named_tuples import LeapSecEntry, SecsSinceEpochUTC, SecsSinceEpochTZ, DateTupleBasic, DateTupleTZ, UnixTimestampUTC

from .calendars.date_base import _init_module_vars as _DateBase_init_module_vars
from .update_timezone_db import DEFAULT_TZDB_UPDATE_CHECK_TIME as _DEFAULT_TZDB_UPDATE_CHECK_TIME
from .update_timezone_db import DEFAULT_TZDB_URL as _DEFAULT_TZDB_URL
from .update_timezone_db import DEFAULT_TZDB_VERSION_URL as _DEFAULT_TZDB_VERSION_URL
from .update_timezone_db import DEFAULT_TZDB_PATH as _DEFAULT_TZDB_PATH
from .update_timezone_db import DEFAULT_TZDB_DOWNLOADED_TIME_PATH as _DEFAULT_TZDB_DOWNLOADED_TIME_PATH
from .update_timezone_db import get_tzdb_data as _Tzdb_get_tzdb_data

_DateBase_init_module_vars()

TIMEZONES: dict[str, dict[str, TimeZone]] = {
  'proleptic_varying': {},
  'proleptic_fixed': {},
  'full_varying': {},
  'full_fixed': {},
}

def update_timezone_data(
    update_check_time: TimeStorageType = _DEFAULT_TZDB_UPDATE_CHECK_TIME,
    tzdb_url: str = _DEFAULT_TZDB_URL,
    version_url: str = _DEFAULT_TZDB_VERSION_URL,
    db_file_path: str = _DEFAULT_TZDB_PATH,
    downloaded_time_file_path: str = _DEFAULT_TZDB_DOWNLOADED_TIME_PATH
  ) -> None:
  new_data = _Tzdb_get_tzdb_data(
    update_check_time,
    tzdb_url,
    version_url,
    db_file_path,
    downloaded_time_file_path
  )
  for key in new_data:
    TIMEZONES[key] = new_data[key]

def update_time_databases() -> None:
  TimeInstant.update_leap_seconds()
  update_timezone_data()
