from typing import Self

from ..fixed_prec import FixedPrec
from .lib import TimeStorageType

class TimeDelta:
  'Class representing the difference between two times, stored using the TAI length of second.'
  
  __slots__ = '_time_delta'
  _time_delta: TimeStorageType
  
  def __init__(self, time_delta: FixedPrec | int | float | str, coerce_to_fixed_prec: bool = True):
    if coerce_to_fixed_prec and not isinstance(time_delta, FixedPrec):
      time_delta = FixedPrec.from_basic(time_delta)
    
    self._time_delta = time_delta
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self._time_delta!r})'
  
  def __str__(self) -> str:
    return f'TD{self._time_delta:+}'
  
  @property
  def time_delta(self) -> TimeStorageType:
    return self._time_delta
  
  def __neg__(self) -> Self:
    return TimeDelta(-self._time_delta)
  
  def __add__(self, other: Self) -> Self:
    return TimeDelta(self._time_delta + other._time_delta)
  
  def __sub__(self, other: Self) -> Self:
    return self + (-other)
  
  def __mul__(self, other) -> Self:
    return TimeDelta(self._time_delta * other)
  
  def __truediv__(self, other) -> Self:
    return TimeDelta(self._time_delta / other)
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    return self._time_delta == other._time_delta
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    return self._time_delta != other._time_delta
  
  def __gt__(self, other: Self):
    return self._time_delta > other._time_delta
  
  def __lt__(self, other: Self):
    return self._time_delta < other._time_delta
  
  def __ge__(self, other: Self):
    return self._time_delta >= other._time_delta
  
  def __le__(self, other: Self):
    return self._time_delta <= other._time_delta
