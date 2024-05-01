from enum import Enum
from functools import lru_cache
from numbers import Integral
from typing import Iterable

from ..fixed_prec import FixedPrec
from ..calendars.jul_greg_base import JulGregBaseDate
from ..calendars.gregorian import GregorianDate
from .lib import TimeStorageType
from .time_instant import time_inst

class TimeZone:
  # static stuff
  
  OffsetDayMode = Enum('OffsetDayMode', (
    'MONTH_AND_DAY',
    'MONTH_WEEK_DAY',
    'MONTH_WEEKDAY_DAY_GE',
    'MONTH_WEEKDAY_DAY_LE',
  ))
  
  @classmethod
  def realize_offset_entry[T: type[JulGregBaseDate]](cls, year: Integral, offset_day_entry: dict[str], date_cls: T = GregorianDate) -> T:
    if offset_day_entry['offset_day_mode'] == cls.OffsetDayMode.MONTH_AND_DAY:
      return date_cls(year, offset_day_entry['month'], offset_day_entry['day'])
    elif offset_day_entry['offset_day_mode'] == cls.OffsetDayMode.MONTH_WEEK_DAY:
      return date_cls.from_month_week_day(
        year, offset_day_entry['month'],
        offset_day_entry['week'], offset_day_entry['day_in_week'],
        from_month_end = offset_day_entry['from_month_end']
      )
    elif offset_day_entry['offset_day_mode'] == cls.OffsetDayMode.MONTH_WEEKDAY_DAY_GE:
      return date_cls.from_month_day_of_week_comp_day(
        year, offset_day_entry['month'],
        offset_day_entry['day'], offset_day_entry['day_in_week'],
        greater_than_equals = True
      )
    elif offset_day_entry['offset_day_mode'] == cls.OffsetDayMode.MONTH_WEEKDAY_DAY_LE:
      return date_cls.from_month_day_of_week_comp_day(
        year, offset_day_entry['month'],
        offset_day_entry['day'], offset_day_entry['day_in_week'],
        greater_than_equals = False
      )
  
  # instance stuff
  
  __slots__ = '_base_utc_offset', '_data_name', '_initial_offset', '_later_offsets'
  _base_utc_offset: FixedPrec
  _data_name: str
  _initial_offset: dict[str]
  _later_offsets: tuple[dict[str], ...]
  
  def __init__(self, base_utc_offset: FixedPrec, initial_offset: dict[str, FixedPrec | int | float | str | None] = None, later_offsets: Iterable[dict[str, OffsetDayMode | Integral | FixedPrec | bool]] = (), coerce_to_fixed_prec: bool = True):
    if coerce_to_fixed_prec and not isinstance(base_utc_offset, FixedPrec):
      self._base_utc_offset = FixedPrec.from_basic(base_utc_offset)
    else:
      self._base_utc_offset = base_utc_offset
    
    self._initial_offset = {}
    
    if initial_offset != None:
      if coerce_to_fixed_prec and not isinstance(initial_offset['utc_offset'], FixedPrec):
        self._initial_offset['utc_offset'] = FixedPrec.from_basic(initial_offset['utc_offset'])
      else:
        self._initial_offset['utc_offset'] = initial_offset['utc_offset']
      
      self._initial_offset['abbreviation'] = initial_offset.get('abbreviation', None)
      self._initial_offset['name'] = initial_offset.get('name', None)
    else:
      self._initial_offset['utc_offset'] = base_utc_offset
      self._initial_offset['abbreviation'] = None
      self._initial_offset['name'] = None
    
    # format for initial_offset:
    # {
    #   'utc_offset': FixedPrec seconds,
    #   'abbreviation': str | None,
    #   'name': str | None,
    # }
    
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
    #     'abbreviation': str | None,
    #     'name': str | None,
    #   }
    # ]
    
    later_offsets_processed = []
    
    for offset_entry in later_offsets:
      offset_entry_processed = {}
      
      offset_entry_processed['offset_day_mode'] = offset_entry['offset_day_mode']
      
      offset_entry_processed['month'] = offset_entry['month']
      if offset_entry_processed['offset_day_mode'] == self.OffsetDayMode.MONTH_AND_DAY:
        offset_entry_processed['day'] = offset_entry['day']
      elif offset_entry_processed['offset_day_mode'] == self.OffsetDayMode.MONTH_WEEK_DAY:
        offset_entry_processed['week'] = offset_entry['week']
        offset_entry_processed['day_in_week'] = offset_entry['day_in_week']
        offset_entry_processed['from_month_end'] = offset_entry['from_month_end']
      elif offset_entry_processed['offset_day_mode'] == self.OffsetDayMode.MONTH_WEEKDAY_DAY_GE:
        offset_entry_processed['day_in_week'] = offset_entry['day_in_week']
        offset_entry_processed['day'] = offset_entry['day']
      elif offset_entry_processed['offset_day_mode'] == self.OffsetDayMode.MONTH_WEEKDAY_DAY_LE:
        offset_entry_processed['day_in_week'] = offset_entry['day_in_week']
        offset_entry_processed['day'] = offset_entry['day']
      else:
        raise ValueError(f'Offset mode {offset_entry_processed['offset_day_mode']} unrecognized')
      
      if coerce_to_fixed_prec and not isinstance(offset_entry['start_time_in_day'], FixedPrec):
        offset_entry_processed['start_time_in_day'] = FixedPrec.from_basic(offset_entry['start_time_in_day'])
      else:
        offset_entry_processed['start_time_in_day'] = offset_entry['start_time_in_day']
      
      if coerce_to_fixed_prec and not isinstance(offset_entry['utc_offset'], FixedPrec):
        offset_entry_processed['utc_offset'] = FixedPrec.from_basic(offset_entry['utc_offset'])
      else:
        offset_entry_processed['utc_offset'] = offset_entry['utc_offset']
      
      offset_entry_processed['abbreviation'] = offset_entry.get('abbreviation', None)
      offset_entry_processed['name'] = offset_entry.get('name', None)
      
      later_offsets_processed.append(offset_entry_processed)
    
    self._later_offsets = tuple(later_offsets_processed)
  
  def __repr__(self):
    return f'{self.__class__.__name__}({self.initial_offset!r}, {self.later_offsets!r})'
  
  def __str__(self):
    return f'TZ: UTC{time_inst.TimeInstant.fixedprec_offset_to_str(self.initial_offset['utc_offset'])} (initial){'; + others' if len(self.later_offsets) > 0 else ''}'
  
  @property
  def base_utc_offset(self) -> FixedPrec:
    return self._base_utc_offset
  
  @property
  def initial_offset(self) -> dict[str, FixedPrec | int | float | str | None]:
    return self._initial_offset
  
  @property
  def later_offsets(self) -> tuple[dict[str], ...]:
    return self._later_offsets
  
  @lru_cache(maxsize = 32)
  def get_offset_utc_times_for_year(self, year: Integral, date_cls: type[JulGregBaseDate] = GregorianDate):
    # format:
    # [
    #   {
    #     'init_offset_start_time_in_year': FixedPrec seconds,
    #     'current_offset_start_time_in_year': FixedPrec seconds,
    #     'current_offset_end_time_in_year': FixedPrec seconds,
    #     'utc_offset': FixedPrec seconds,
    #     'dst_transition_offset': FixedPrec seconds offset2 - offset1,
    #   }
    # ]
    
    offset_times = []
    
    current_offset = self.initial_offset['utc_offset']
    year_start_time = time_inst.TimeInstant.date_tuple_to_epoch_instant(year, 1, 1, 0, 0, 0, 0, date_cls = GregorianDate)
    
    for later_offset_entry in self.later_offsets:
      later_date = self.realize_offset_entry(year, later_offset_entry, date_cls = date_cls)
      
      later_instant = time_inst.TimeInstant.date_tuple_to_epoch_instant(
        later_date.year, later_date.month, later_date.day,
        0, 0, 0, 0,
        date_cls = date_cls
      )
      
      later_time = later_instant + later_offset_entry['start_time_in_day'] - (current_offset - self.initial_offset['utc_offset'])
      init_offset_start_time_in_year = later_time - year_start_time
      current_offset_start_time_in_year = init_offset_start_time_in_year + (current_offset - self.initial_offset['utc_offset'])
      utc_offset = later_offset_entry['utc_offset']
      dst_transition_offset = utc_offset - current_offset
      current_offset_end_time_in_year = current_offset_start_time_in_year + dst_transition_offset
      current_offset_min_time_in_year = min(current_offset_start_time_in_year, current_offset_end_time_in_year)
      offset_times.append({
        'init_offset_start_time_in_year': init_offset_start_time_in_year,
        'current_offset_start_time_in_year': current_offset_start_time_in_year,
        'current_offset_end_time_in_year': current_offset_end_time_in_year,
        'current_offset_min_time_in_year': current_offset_min_time_in_year,
        'utc_offset': utc_offset,
        'dst_transition_offset': dst_transition_offset,
        'abbreviation': later_offset_entry['abbreviation'],
        'name': later_offset_entry['name'],
      })
      current_offset = later_offset_entry['utc_offset']
    
    return offset_times
