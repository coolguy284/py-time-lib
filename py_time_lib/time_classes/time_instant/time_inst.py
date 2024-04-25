from datetime import datetime, UTC as datetime_UTC
from time import time_ns
from typing import Self

from ...fixed_prec import FixedPrec
from ...constants import NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX as _NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX
from ...constants import NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX as _NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX
from .time_inst_jd_ts import TimeInstantJulianDateAndUnixTimestamp
from .time_inst_fmt_str import TimeInstantFormatString

class TimeInstant(TimeInstantJulianDateAndUnixTimestamp, TimeInstantFormatString):
  'Class representing an instant of time. Modeled after TAI, with epoch at jan 1, 1 BCE (year 0). Stores seconds since epoch.'
  
  # static stuff
  
  NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX = _NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX
  NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX = _NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX
  
  # instance stuff
  
  __slots__ = ()
  
  def __init__(self, time: FixedPrec | int | float | str | datetime, coerce_to_fixed_prec: bool = True):
    if isinstance(time, datetime):
      time = self.from_datetime(time)._time
    elif coerce_to_fixed_prec and not isinstance(time, FixedPrec):
      time = FixedPrec.from_basic(time)
    
    self._time = time
  
  @classmethod
  def from_datetime(cls, datetime_obj: datetime) -> Self:
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

TimeInstant._init_class_vars()
