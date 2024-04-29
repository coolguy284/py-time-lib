from datetime import datetime, UTC as datetime_UTC
from time import time_ns, struct_time
from typing import Self

from ...fixed_prec import FixedPrec
from ...constants import NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX as _NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX
from ...constants import NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX as _NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from .time_inst_jd_ts import TimeInstantJulianDateAndUnixTimestamp
from .time_inst_fmt_str import TimeInstantFormatString
from ..time_zone import TimeZone

class TimeInstant(TimeInstantJulianDateAndUnixTimestamp, TimeInstantFormatString):
  'Class representing an instant of time. Modeled after TAI, with epoch at jan 1, 1 BCE (year 0). Stores seconds since epoch.'
  
  # static stuff
  
  NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX = _NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX
  NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX = _NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX
  
  # instance stuff
  
  __slots__ = ()
  
  def __init__(self, time: FixedPrec | int | float | str | datetime | struct_time, coerce_to_fixed_prec: bool = True):
    if isinstance(time, datetime):
      time = self.from_datetime(time)._time
    elif isinstance(time, struct_time):
      time = self.from_struct_time(time)._time
    elif coerce_to_fixed_prec and not isinstance(time, FixedPrec):
      time = FixedPrec.from_basic(time)
    
    self._time = time
  
  @classmethod
  def from_datetime(cls, datetime_obj: datetime, round_invalid_leap_time_upwards: bool = True) -> Self:
    if datetime_obj.tzinfo != datetime_UTC:
      new_datetime_obj = datetime_obj.astimezone(datetime_UTC)
    else:
      new_datetime_obj = datetime_obj
    
    return cls.from_date_tuple_utc(
      new_datetime_obj.year,
      new_datetime_obj.month,
      new_datetime_obj.day,
      new_datetime_obj.hour,
      new_datetime_obj.minute,
      new_datetime_obj.second,
      FixedPrec(new_datetime_obj.microsecond, cls.NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX),
      round_invalid_time_upwards = round_invalid_leap_time_upwards
    )
  
  @classmethod
  def from_struct_time(cls, struct_time_obj: struct_time, round_invalid_leap_time_upwards: bool = True, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    return cls.from_date_tuple_tz(
      TimeZone(struct_time_obj.tm_gmtoff),
      struct_time_obj.tm_year,
      struct_time_obj.tm_mon,
      struct_time_obj.tm_mday,
      struct_time_obj.tm_hour,
      struct_time_obj.tm_min,
      struct_time_obj.tm_sec,
      0,
      round_invalid_leap_time_upwards = round_invalid_leap_time_upwards,
      date_cls = date_cls
    )
  
  @classmethod
  def now(cls) -> Self:
    return cls.from_unix_timestamp(FixedPrec(time_ns(), cls.NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX))
  
  def to_datetime(self) -> datetime:
    utc_info = self.to_utc_info()
    
    # adjust time forward to prevent erroring on the leap second
    if utc_info['positive_leap_second_occurring']:
      self_adjusted = self.__class__.from_utc_secs_since_epoch(utc_info['utc_seconds_since_epoch'], True)
    else:
      self_adjusted = self
    
    year, month, day, hour, minute, second, frac_second = self_adjusted.to_date_tuple_utc()
    
    return datetime(year, month, day, hour, minute, second, int(frac_second * self.NOMINAL_MICROSECS_PER_SEC), datetime_UTC)
  
  def to_struct_time(self, time_zone: TimeZone | None = None, date_cls: type[JulGregBaseDate] = GregorianDate):
    if time_zone == None:
      year, month, day, hour, minute, second, _ = self.to_date_tuple_utc(date_cls = date_cls)
      date = date_cls(year, month, day)
      return struct_time(
        (year, month, day, hour, minute, second, date.iso_day_of_week() - 1, date.ordinal_date(), 0),
        {
          'tm_zone': 'UTC',
          'tm_gmtoff': 0,
        }
      )
    else:
      year, month, day, hour, minute, second, _, _ = self.to_date_tuple_tz(time_zone, date_cls = date_cls)
      date = date_cls(year, month, day)
      current_tz_offset, current_tz_abbr = self.current_tz_offset(time_zone, date_cls = date_cls)
      return struct_time(
        (year, month, day, hour, minute, second, date.iso_day_of_week() - 1, date.ordinal_date(), current_tz_offset != time_zone.base_utc_offset),
        {
          'tm_zone': 'NULL' if current_tz_abbr == None else current_tz_abbr,
          'tm_gmtoff': int(current_tz_offset),
        }
      )

TimeInstant._init_class_vars()
