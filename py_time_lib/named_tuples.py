from numbers import Integral
from typing import NamedTuple

from .fixed_prec import FixedPrec
from .time_classes.lib import TimeStorageType

# date tuples

class MonthWeekDate(NamedTuple):
  year: Integral
  month: Integral
  week: Integral
  day_of_week: Integral

# time tuples

class LeapSecEntry(NamedTuple):
  date_str: str
  time_in_day_secs: FixedPrec
  leap_sec_delta: FixedPrec

class UT1TAIOffsetEntry(NamedTuple):
  secs_since_epoch: FixedPrec
  ut1_minus_tai: FixedPrec

class TAIUT1OffsetEntry(NamedTuple):
  secs_since_epoch: FixedPrec
  tai_minus_ut1: FixedPrec

class SecsSinceEpochUTC(NamedTuple):
  secs_since_epoch: TimeStorageType
  leap_second_fold: bool

class SecsSinceEpochTZ(NamedTuple):
  secs_since_epoch: TimeStorageType
  dst_second_fold: bool
  leap_second_fold: bool

class SecsSinceEpochSmearTZ(NamedTuple):
  secs_since_epoch: TimeStorageType
  dst_second_fold: bool

class DateTupleBasic(NamedTuple):
  year: Integral
  month: Integral
  day: Integral
  hour: Integral
  minute: Integral
  second: Integral
  frac_second: TimeStorageType

class DateTupleTZ(NamedTuple):
  year: Integral
  month: Integral
  day: Integral
  hour: Integral
  minute: Integral
  second: Integral
  frac_second: TimeStorageType
  dst_second_fold: bool

class DateTupleFormatString(NamedTuple):
  year: Integral
  month: Integral
  day: Integral
  hour: Integral
  minute: Integral
  second: Integral
  frac_second: TimeStorageType
  tz_offset: TimeStorageType | None
  tz_name: str | None

class CurrentTZOffset(NamedTuple):
  offset: FixedPrec
  abbreviation: str | None

class UnixTimestampUTC(NamedTuple):
  unix_secs_since_epoch: TimeStorageType
  leap_second_fold: bool

class JulianDateUTC(NamedTuple):
  julian_date: TimeStorageType
  leap_second_fold: bool

class ReducedJulianDateUTC(NamedTuple):
  reduced_julian_date: TimeStorageType
  leap_second_fold: bool

class ModifiedJulianDateUTC(NamedTuple):
  modified_julian_date: TimeStorageType
  leap_second_fold: bool
