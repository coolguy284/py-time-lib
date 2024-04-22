from enum import Enum
from numbers import Integral
from typing import Iterable

from ..fixed_prec import FixedPrec
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
    return f'TZ: UTC+{time_inst.TimeInstant.fixedprec_offset_to_str(self.initial_utc_offset)} (initial)'
  
  @property
  def initial_utc_offset(self) -> FixedPrec:
    return self._initial_utc_offset
  
  @property
  def later_offsets(self) -> tuple[dict[str], ...]:
    return self._later_offsets
