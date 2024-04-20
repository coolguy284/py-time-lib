from numbers import Integral
from typing import Self
from ...calendars.date_base import DateBase
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType

from .time_inst_leap_sec import TimeInstantLeapSec

class TimeInstantDateTuple(TimeInstantLeapSec):
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_date_tuple_tai(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, date_cls: type[DateBase] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a tai TimeInstant.'
    date = date_cls(year, month, day)
    time = date.days_since_epoch * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    return cls(time)
  
  @classmethod
  def from_date_tuple_utc(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, round_invalid_time_upwards: bool = True, date_cls: type[DateBase] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a utc TimeInstant. Does not handle leap seconds that occur during the day.'
    date = date_cls(year, month, day)
    time = date.days_since_epoch * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    date_mins = cls.days_h_m_to_mins_since_epoch(date.days_since_epoch, hour, minute)
    if date_mins in cls.LEAP_SECONDS_DICT:
      leap_entries = cls.LEAP_SECONDS_DICT[date_mins]
      leap_delta = leap_entries[-1]['utc_delta']
      if leap_delta < 0:
        # positive leap second
        if hour * cls.NOMINAL_SECS_PER_HOUR + minute * cls.NOMINAL_SECS_PER_MIN + second + frac_second < -leap_delta:
          leap_fold = True
        else:
          leap_fold = False
      else:
        leap_fold = False
    else:
      leap_fold = False
    return cls.from_utc_secs_since_epoch(time, second_fold = leap_fold, round_invalid_time_upwards = round_invalid_time_upwards)
  
  def to_date_tuple_tai(self, date_cls: type[DateBase] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    'Returns a date tuple in the TAI timezone (as math is easiest for this).'
    return self.epoch_instant_to_date_tuple(self._time, date_cls = date_cls)
  
  def to_date_tuple_utc(self, date_cls: type[DateBase] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType]:
    'Returns a date tuple in the UTC timezone. Does not handle leap seconds that occur during the day.'
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
