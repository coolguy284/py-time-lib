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

class UT1OffsetEntry(NamedTuple):
  secs_since_epoch: FixedPrec
  ut1_minus_tai: FixedPrec

class SecsSinceEpochUTC(NamedTuple):
  secs_since_epoch: TimeStorageType
  leap_second_fold: bool

class SecsSinceEpochTZ(NamedTuple):
  secs_since_epoch: TimeStorageType
  dst_second_fold: bool
  leap_second_fold: bool

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

class UnixTimestampUTC(NamedTuple):
  unix_secs_since_epoch: TimeStorageType
  leap_second_fold: bool
