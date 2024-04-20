from datetime import datetime, UTC as datetime_UTC
from time import time_ns
from typing import Self

from ...fixed_prec import FixedPrec
from .time_inst_jd_ts import TimeInstantJulianDateAndUnixTimestamp
from .time_inst_fmt_str import TimeInstantFormatString

class TimeInstant(TimeInstantJulianDateAndUnixTimestamp, TimeInstantFormatString):
  'Class representing an instant of time. Modeled after TAI, with epoch at jan 1, 1 BCE (year 0). Stores seconds since epoch.'
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_datetime(cls, datetime_obj: datetime) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def now(cls) -> Self:
    return cls.from_unix_timestamp(FixedPrec(time_ns(), 9))
  
  def to_datetime(self) -> datetime:
    utc_info = self.to_utc_info()
    if utc_info['positive_leap_second_occurring']:
      self_adjusted = self.__class__.from_utc_secs_since_epoch(utc_info['utc_seconds_since_epoch'], True)
    else:
      self_adjusted = self
    
    year, month, day, hour, minute, second, frac_second = self_adjusted.to_date_tuple_utc()
    
    return datetime(year, month, day, hour, minute, second, int(frac_second * self.NOMINAL_MICROSECS_PER_SEC), datetime_UTC)

TimeInstant._init_class_vars()
