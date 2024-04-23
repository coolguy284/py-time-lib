from enum import Enum
from numbers import Integral
from typing import Iterable

from ..fixed_prec import FixedPrec
from ..calendars.jul_greg_base import JulGregBaseDate
from ..calendars.gregorian import GregorianDate
from .time_instant import time_inst

class TimeZone:
  # static stuff
  
  OffsetDayMode = Enum('OffsetDayMode', [
    'MONTH_AND_DAY',
    'MONTH_WEEK_DAY',
  ])
  
  # instance stuff
  
  __slots__ = '_initial_utc_offset', '_later_offsets'
  _initial_utc_offset: FixedPrec
  _later_offsets: tuple[dict[str], ...]
  
  def __init__(self, initial_utc_offset: FixedPrec | int | float | str, later_offsets: Iterable[dict[str, OffsetDayMode | Integral | FixedPrec | bool]] = (), coerce_to_fixed_prec: bool = True):
    if coerce_to_fixed_prec and not isinstance(initial_utc_offset, FixedPrec):
      self._initial_utc_offset = FixedPrec.from_basic(initial_utc_offset)
    else:
      self._initial_utc_offset = initial_utc_offset
    
    # format for later_offsets:
    # [
    #   {
    #     'offset_day_mode': OffsetDayMode,
    #     if offset_day_mode == MONTH_AND_DAY:
    #       'month': Integer,
    #       'day': Integer,
    #     elif offset_day_mode == MONTH_WEEK_DAY:
    #       'month': Integer,
    #       'week': Integer,
    #       'day_in_week': Integer,
    #       'from_month_end': bool,
    #     'start_time_in_day': FixedPrec seconds,
    #     'utc_offset': FixedPrec seconds,
    #   }
    # ]
    
    later_offsets_processed = []
    
    for offset_entry in later_offsets:
      offset_entry_processed = {}
      
      offset_entry_processed['offset_day_mode'] = offset_entry['offset_day_mode']
      
      if offset_entry_processed['offset_day_mode'] == self.OffsetDayMode.MONTH_AND_DAY:
        offset_entry_processed['month'] = offset_entry['month']
        offset_entry_processed['day'] = offset_entry['day']
      elif offset_entry_processed['offset_day_mode'] == self.OffsetDayMode.MONTH_WEEK_DAY:
        offset_entry_processed['month'] = offset_entry['month']
        offset_entry_processed['week'] = offset_entry['week']
        offset_entry_processed['day_in_week'] = offset_entry['day_in_week']
        offset_entry_processed['from_month_end'] = offset_entry['from_month_end']
      else:
        raise Exception(f'Offset mode {offset_entry_processed['offset_day_mode']} unrecognized')
      
      if coerce_to_fixed_prec and not isinstance(offset_entry['start_time_in_day'], FixedPrec):
        offset_entry_processed['start_time_in_day'] = FixedPrec.from_basic(offset_entry['start_time_in_day'])
      else:
        offset_entry_processed['start_time_in_day'] = offset_entry['start_time_in_day']
      
      if coerce_to_fixed_prec and not isinstance(offset_entry['utc_offset'], FixedPrec):
        offset_entry_processed['utc_offset'] = FixedPrec.from_basic(offset_entry['utc_offset'])
      else:
        offset_entry_processed['utc_offset'] = offset_entry['utc_offset']
      
      later_offsets_processed.append(offset_entry_processed)
    
    self._later_offsets = tuple(later_offsets_processed)
  
  def __repr__(self):
    return f'{self.__class__.__name__}({self.initial_utc_offset!r}, {self.later_offsets!r})'
  
  def __str__(self):
    return f'TZ: UTC+{time_inst.TimeInstant.fixedprec_offset_to_str(self.initial_utc_offset)} (initial){'; + others' if len(self.later_offsets) > 0 else ''}'
  
  @property
  def initial_utc_offset(self) -> FixedPrec:
    return self._initial_utc_offset
  
  @property
  def later_offsets(self) -> tuple[dict[str], ...]:
    return self._later_offsets
  
  def get_offset_utc_times_for_year(self, year, date_cls: type[JulGregBaseDate] = GregorianDate):
    # format:
    # [
    #   {
    #     'init_offset_time_in_year': FixedPrec seconds,
    #     'current_offset_time_in_year': FixedPrec seconds,
    #     'utc_offset': FixedPrec seconds,
    #     'dst_transition_offset': FixedPrec seconds offset2 - offset1,
    #   }
    # ]
    
    offset_times = []
    
    current_offset = self.initial_utc_offset
    year_start_time = time_inst.TimeInstant.date_tuple_to_epoch_instant(year, 1, 1, 0, 0, 0, 0, date_cls = GregorianDate) - current_offset
    for later_offset_entry in self.later_offsets:
      if later_offset_entry['offset_day_mode'] == self.OffsetDayMode.MONTH_AND_DAY:
        later_instant = time_inst.TimeInstant.date_tuple_to_epoch_instant(
          year, later_offset_entry['month'], later_offset_entry['day'],
          0, 0, 0, 0,
          date_cls = GregorianDate
        )
      elif later_offset_entry['offset_day_mode'] == self.OffsetDayMode.MONTH_WEEK_DAY:
        later_instant = time_inst.TimeInstant.date_tuple_to_epoch_instant(
          *date_cls.from_month_week_day(
            year, later_offset_entry['month'], later_offset_entry['week'], later_offset_entry['day_in_week'],
            from_month_end = later_offset_entry['from_month_end']
          ).to_date_tuple(),
          0, 0, 0, 0,
          date_cls = GregorianDate
        )
      later_time = later_instant - current_offset
      init_offset_time_in_year = later_time - year_start_time
      current_offset_time_in_year = init_offset_time_in_year + (current_offset - self.initial_utc_offset)
      offset_times.append({
        'init_offset_time_in_year': init_offset_time_in_year,
        'current_offset_time_in_year': current_offset_time_in_year,
        'utc_offset': later_offset_entry['utc_offset'],
        'dst_transition_offset': later_offset_entry['utc_offset'] - current_offset,
      })
      current_offset = later_offset_entry['utc_offset']
    
    return offset_times
