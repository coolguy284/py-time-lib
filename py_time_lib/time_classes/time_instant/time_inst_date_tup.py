from numbers import Integral
from typing import Self

from ...fixed_prec import FixedPrec
from ...calendars.date_base import DateBase
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType
from .time_inst_leap_sec import TimeInstantLeapSec

class TimeInstantDateTuple(TimeInstantLeapSec):
  # static stuff
  
  @classmethod
  def epoch_instant_to_date_tuple(cls, secs_since_epoch: FixedPrec, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    days_since_epoch, time_since_day_start = divmod(secs_since_epoch, cls.NOMINAL_SECS_PER_DAY)
    date = date_cls.from_days_since_epoch(int(days_since_epoch))
    hour, remainder = divmod(time_since_day_start, cls.NOMINAL_SECS_PER_HOUR)
    minute, remainder = divmod(remainder, cls.NOMINAL_SECS_PER_MIN)
    second, frac_second = divmod(remainder, 1)
    return *date.to_date_tuple(), int(hour), int(minute), int(second), frac_second
  
  @classmethod
  def date_tuple_to_epoch_instant(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, date_cls: type[JulGregBaseDate] = GregorianDate) -> TimeStorageType:
    date = date_cls(year, month, day)
    time = date.days_since_epoch * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    return time
  
  @classmethod
  def days_h_m_to_mins_since_epoch(cls, days_since_epoch: Integral, hour: Integral, minute: Integral) -> int:
    return days_since_epoch * cls.NOMINAL_MINS_PER_DAY + hour * cls.NOMINAL_MINS_PER_HOUR + minute
  
  @classmethod
  def mins_since_epoch_to_days_h_m(cls, mins_since_epoch: Integral) -> tuple[int, int, int]:
    hrs_since_epoch, minute = divmod(mins_since_epoch, cls.NOMINAL_MINS_PER_HOUR)
    days_since_epoch, hour = divmod(hrs_since_epoch, cls.NOMINAL_HOURS_PER_DAY)
    return days_since_epoch, hour, minute
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_date_tuple_tai(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a tai TimeInstant.'
    return cls(cls.date_tuple_to_epoch_instant(year, month, day, hour, minute, second, frac_second, date_cls = date_cls))
  
  @classmethod
  def from_date_tuple_utc(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, round_invalid_time_upwards: bool = True, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a TimeInstant. Does not handle leap seconds that occur not on a minute boundary.'
    
    date = date_cls(year, month, day)
    date_mins = cls.days_h_m_to_mins_since_epoch(date.days_since_epoch, hour, minute)
    
    time = date_mins * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    
    if date_mins in cls.LEAP_SECONDS_DICT:
      leap_entries = cls.LEAP_SECONDS_DICT[date_mins]
      leap_delta = leap_entries[-1]['utc_delta']
      if leap_delta < 0:
        # positive leap second
        if second + frac_second < -leap_delta:
          leap_fold = True
        else:
          leap_fold = False
      else:
        leap_fold = False
    else:
      leap_fold = False
    
    return cls.from_utc_secs_since_epoch(time, second_fold = leap_fold, round_invalid_time_upwards = round_invalid_time_upwards)
  
  def to_date_tuple_tai(self, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    'Returns a date tuple in the TAI timezone (as math is easiest for this).'
    return self.epoch_instant_to_date_tuple(self._time, date_cls = date_cls)
  
  def to_date_tuple_utc(self, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    'Returns a date tuple in the UTC timezone. Does not handle leap seconds that occur not on a minute boundary.'
    utc_info = self.to_utc_info()
    utc_secs_since_epoch = utc_info['utc_seconds_since_epoch']
    if utc_info['positive_leap_second_occurring']:
      utc_secs_since_epoch -= 1
    *date, hour, minute, second, frac_second = self.epoch_instant_to_date_tuple(utc_secs_since_epoch, date_cls = date_cls)
    if utc_info['positive_leap_second_occurring']:
      second += 1
      second_addl, frac_second = divmod(frac_second + (self._time - utc_info['last_leap_transition_time']), 1)
      second = int(second + second_addl)
    return *date, hour, minute, second, frac_second
  
  def get_date_object_tai[T: DateBase](self, date_cls: type[T] = GregorianDate) -> T:
    days_since_epoch, _ = divmod(self.time, self.NOMINAL_SECS_PER_DAY)
    return date_cls.from_days_since_epoch(int(days_since_epoch))
