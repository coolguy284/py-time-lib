from numbers import Integral
from typing import Self

from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType
from .. import time_zone
from .time_inst_date_tup import TimeInstantDateTuple

class TimeInstantTimeZones(TimeInstantDateTuple):
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_tz_secs_since_epoch(
      cls,
      time_zone: time_zone.TimeZone,
      tz_secs_since_epoch: TimeStorageType,
      dst_second_fold: bool = False,
      leap_second_fold: bool = False,
      round_invalid_dst_time_upwards: bool = True,
      round_invalid_leap_time_upwards: bool = True
    ) -> Self:
    if len(time_zone.later_offsets) > 0:
      raise Exception('Variable timezones not supported')
    secs_since_epoch = tz_secs_since_epoch - time_zone.initial_utc_offset
    return cls.from_utc_secs_since_epoch(secs_since_epoch, leap_second_fold, round_invalid_time_upwards = round_invalid_leap_time_upwards)
  
  @classmethod
  def from_date_tuple_tz(
      cls,
      time_zone: time_zone.TimeZone,
      year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
      dst_second_fold: bool = False,
      round_invalid_dst_time_upwards: bool = True,
      round_invalid_leap_time_upwards: bool = True,
      date_cls: type[JulGregBaseDate] = GregorianDate):
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a TimeInstant. Does not handle leap seconds that occur not on a minute boundary, or timezones not on a minute offset.'
    if len(time_zone.later_offsets) > 0:
      raise Exception('Variable timezones not supported')
    date = date_cls(year, month, day)
    time = date.days_since_epoch * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    time -= time_zone.initial_utc_offset
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
    return cls.from_utc_secs_since_epoch(time, second_fold = leap_fold, round_invalid_time_upwards = round_invalid_leap_time_upwards)
  
  def to_tz_secs_since_epoch(self, time_zone: time_zone.TimeZone) -> tuple[TimeStorageType, bool, bool]:
    'Returns a tuple of the form (secs_since_epoch, dst_second_fold, leap_second_fold).'
    if len(time_zone.later_offsets) > 0:
      raise Exception('Variable timezones not supported')
    secs_since_epoch, leap_second_fold = self.to_utc_secs_since_epoch()
    tz_secs_since_epoch = secs_since_epoch + time_zone.initial_utc_offset
    return tz_secs_since_epoch, False, leap_second_fold
  
  def to_date_tuple_tz(self, time_zone: time_zone.TimeZone, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType, bool]:
    'Returns a date tuple in a timezone. Does not handle leap seconds that occur not on a minute boundary, or timezones not on a minute offset.'
    if len(time_zone.later_offsets) > 0:
      raise Exception('Variable timezones not supported')
    utc_info = self.to_utc_info()
    utc_secs_since_epoch = utc_info['utc_seconds_since_epoch'] + time_zone.initial_utc_offset
    if utc_info['positive_leap_second_occurring']:
      utc_secs_since_epoch -= 1
    *date, hour, minute, second, frac_second = self.epoch_instant_to_date_tuple(utc_secs_since_epoch, date_cls = date_cls)
    if utc_info['positive_leap_second_occurring']:
      second += 1
      second_addl, frac_second = divmod(frac_second + (self._time - utc_info['last_leap_transition_time']), 1)
      second = int(second + second_addl)
    return *date, hour, minute, second, frac_second
