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
  
  def __init__(self, initial_utc_offset: FixedPrec | int | float | str, later_offsets: Iterable[dict[str, OffsetDayMode | Integral | FixedPrec]], coerce_to_fixed_prec: bool = True):
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
    #     'time_in_day': FixedPrec seconds,
    #   }
    # ]
    self._later_offsets = tuple(later_offsets)
  
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
