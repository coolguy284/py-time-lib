from numbers import Integral
from typing import Self

from ...lib_funcs import binary_search
from ...exceptions import TimeUnmappableError
from ...fixed_prec import FixedPrec
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType
from .. import time_zone
from .time_inst_named_tup import SecsSinceEpochTZ, DateTupleTZ
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
      round_invalid_leap_time_upwards: bool = True,
      date_cls: type[JulGregBaseDate] = GregorianDate
    ) -> Self:
    if len(time_zone.later_offsets) == 0:
      initial_tz_secs_since_epoch = tz_secs_since_epoch
    else:
      prelim_year = cls.epoch_instant_to_date_tuple(tz_secs_since_epoch, date_cls = date_cls)[0]
      prelim_year_start_time = cls.date_tuple_to_epoch_instant(prelim_year, 1, 1, 0, 0, 0, 0, date_cls = date_cls)
      current_offset_time_in_year = tz_secs_since_epoch - prelim_year_start_time
      offset_times = time_zone.get_offset_utc_times_for_year(prelim_year, date_cls = date_cls)
      
      if offset_times[0]['current_offset_min_time_in_year'] > current_offset_time_in_year:
        initial_tz_secs_since_epoch = tz_secs_since_epoch
      else:
        dst_table_index = binary_search(lambda x: current_offset_time_in_year >= offset_times[x]['current_offset_min_time_in_year'], 0, len(offset_times))
        dst_entry = offset_times[dst_table_index]
        
        if dst_entry['dst_transition_offset'] >= 0:
          # spring forward
          if current_offset_time_in_year - dst_entry['current_offset_start_time_in_year'] < dst_entry['dst_transition_offset']:
            # in middle of spring forward, this time does not map to a physical time
            if round_invalid_dst_time_upwards:
              current_offset_time_in_year = dst_entry['current_offset_end_time_in_year']
              tz_secs_since_epoch = current_offset_time_in_year + prelim_year_start_time
            else:
              raise TimeUnmappableError('tz time does not map to utc')
          
          # past the end of spring forward or adjusted to the end
          initial_tz_secs_since_epoch = tz_secs_since_epoch - (dst_entry['utc_offset'] - time_zone.initial_utc_offset)
        else:
          # fall back
          if dst_second_fold or current_offset_time_in_year >= dst_entry['current_offset_start_time_in_year']:
            initial_tz_secs_since_epoch = tz_secs_since_epoch - (dst_entry['utc_offset'] - time_zone.initial_utc_offset)
          else:
            initial_tz_secs_since_epoch = tz_secs_since_epoch - (dst_entry['utc_offset'] - time_zone.initial_utc_offset) + dst_entry['dst_transition_offset']
    
    secs_since_epoch = initial_tz_secs_since_epoch - time_zone.initial_utc_offset
    
    return cls.from_utc_secs_since_epoch(secs_since_epoch, leap_second_fold, round_invalid_time_upwards = round_invalid_leap_time_upwards)
  
  @classmethod
  def from_date_tuple_tz(
      cls,
      time_zone: time_zone.TimeZone,
      year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
      dst_second_fold: bool = False,
      round_invalid_dst_time_upwards: bool = True,
      round_invalid_leap_time_upwards: bool = True,
      date_cls: type[JulGregBaseDate] = GregorianDate
    ) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a TimeInstant. Does not handle leap seconds that occur not on a minute boundary, or timezones not on a minute offset.'
    
    date = date_cls(year, month, day)
    date_mins = cls.days_h_m_to_mins_since_epoch(date.days_since_epoch, hour, minute)
    
    time = date_mins * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    
    offset = cls.from_tz_secs_since_epoch(
      time_zone,
      time,
      dst_second_fold = dst_second_fold,
      leap_second_fold = False,
      round_invalid_dst_time_upwards = round_invalid_dst_time_upwards,
      round_invalid_leap_time_upwards = round_invalid_leap_time_upwards,
      date_cls = date_cls
    ).current_tz_offset(time_zone, date_cls = date_cls)
    
    utc_date_mins = date_mins - (offset // cls.NOMINAL_SECS_PER_MIN)
    
    if utc_date_mins in cls.LEAP_SECONDS_DICT:
      leap_entries = cls.LEAP_SECONDS_DICT[utc_date_mins]
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
    
    return cls.from_tz_secs_since_epoch(time_zone, time, dst_second_fold = dst_second_fold, leap_second_fold = leap_fold, round_invalid_dst_time_upwards = round_invalid_dst_time_upwards, round_invalid_leap_time_upwards = round_invalid_leap_time_upwards, date_cls = date_cls)
  
  def to_tz_secs_since_epoch(self, time_zone: time_zone.TimeZone, date_cls: type[JulGregBaseDate] = GregorianDate) -> SecsSinceEpochTZ:
    'Returns a tuple of the form (secs_since_epoch, dst_second_fold, leap_second_fold).'
    
    secs_since_epoch, leap_second_fold = self.to_utc_secs_since_epoch()
    initial_tz_secs_since_epoch = secs_since_epoch + time_zone.initial_utc_offset
    
    if len(time_zone.later_offsets) == 0:
      tz_secs_since_epoch = initial_tz_secs_since_epoch
      dst_second_fold = False
    else:
      prelim_year = self.epoch_instant_to_date_tuple(initial_tz_secs_since_epoch, date_cls = date_cls)[0]
      prelim_year_start_time = self.date_tuple_to_epoch_instant(prelim_year, 1, 1, 0, 0, 0, 0, date_cls = date_cls)
      init_offset_time_in_year = initial_tz_secs_since_epoch - prelim_year_start_time
      offset_times = time_zone.get_offset_utc_times_for_year(prelim_year, date_cls = date_cls)
      if offset_times[0]['init_offset_start_time_in_year'] > init_offset_time_in_year:
        tz_secs_since_epoch = initial_tz_secs_since_epoch
        dst_second_fold = False
      else:
        dst_table_index = binary_search(lambda x: init_offset_time_in_year >= offset_times[x]['init_offset_start_time_in_year'], 0, len(offset_times))
        dst_entry = offset_times[dst_table_index]
        tz_secs_since_epoch = initial_tz_secs_since_epoch + (dst_entry['utc_offset'] - time_zone.initial_utc_offset)
        if dst_entry['dst_transition_offset'] < 0:
          if init_offset_time_in_year - dst_entry['init_offset_start_time_in_year'] < -dst_entry['dst_transition_offset']:
            dst_second_fold = True
          else:
            dst_second_fold = False
        else:
          dst_second_fold = False
    
    return SecsSinceEpochTZ(tz_secs_since_epoch, dst_second_fold, leap_second_fold)
  
  def to_date_tuple_tz(self, time_zone: time_zone.TimeZone, date_cls: type[JulGregBaseDate] = GregorianDate) -> DateTupleTZ:
    'Returns a date tuple in a timezone. Does not handle leap seconds that occur not on a minute boundary, or timezones not on a minute offset.'
    utc_info = self.to_utc_info()
    tz_secs_since_epoch, dst_second_fold, _ = self.to_tz_secs_since_epoch(time_zone, date_cls = date_cls)
    if utc_info['positive_leap_second_occurring']:
      time_in_leap = self._time - utc_info['last_leap_transition_time']
      tz_secs_since_epoch -= 1 + time_in_leap
    *date, hour, minute, second, frac_second = self.epoch_instant_to_date_tuple(tz_secs_since_epoch, date_cls = date_cls)
    if utc_info['positive_leap_second_occurring']:
      second += 1
      second_addl, frac_second = divmod(frac_second + time_in_leap, 1)
      second = int(second + second_addl)
    return DateTupleTZ(*date, hour, minute, second, frac_second, dst_second_fold)
  
  def current_tz_offset(self, time_zone: time_zone.TimeZone, date_cls: type[JulGregBaseDate] = GregorianDate) -> FixedPrec:
    secs_since_epoch, _ = self.to_utc_secs_since_epoch()
    initial_tz_secs_since_epoch = secs_since_epoch + time_zone.initial_utc_offset
    offset = time_zone.initial_utc_offset
    
    if len(time_zone.later_offsets) != 0:
      prelim_year = self.epoch_instant_to_date_tuple(initial_tz_secs_since_epoch, date_cls = date_cls)[0]
      prelim_year_start_time = self.date_tuple_to_epoch_instant(prelim_year, 1, 1, 0, 0, 0, 0, date_cls = date_cls)
      init_offset_time_in_year = initial_tz_secs_since_epoch - prelim_year_start_time
      offset_times = time_zone.get_offset_utc_times_for_year(prelim_year, date_cls = date_cls)
      if offset_times[0]['init_offset_start_time_in_year'] <= init_offset_time_in_year:
        dst_table_index = binary_search(lambda x: init_offset_time_in_year >= offset_times[x]['init_offset_start_time_in_year'], 0, len(offset_times))
        dst_entry = offset_times[dst_table_index]
        offset += (dst_entry['utc_offset'] - time_zone.initial_utc_offset)
    
    return offset
