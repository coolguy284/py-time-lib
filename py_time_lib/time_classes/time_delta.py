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
    return self.__class__(-self._time_delta)
  
  def __add__(self, other: Self) -> Self:
    if hasattr(other, 'time_delta'):
      try:
        return self.__class__(self._time_delta + other.time_delta)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __sub__(self, other: Self) -> Self:
    try:
      return self + (-other)
    except TypeError:
      return NotImplemented
  
  def __mul__(self, other) -> Self:
    if hasattr(other, 'time_delta'):
      return NotImplemented
    else:
      try:
        return self.__class__(self._time_delta * other)
      except TypeError:
        return NotImplemented
  
  def __truediv__(self, other) -> Self:
    if hasattr(other, 'time_delta'):
      return NotImplemented
    else:
      try:
        return self.__class__(self._time_delta / other)
      except TypeError:
        return NotImplemented
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    if hasattr(other, 'time_delta'):
      return self._time_delta == other.time_delta
    else:
      return NotImplemented
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    if hasattr(other, 'time_delta'):
      return self._time_delta != other.time_delta
    else:
      return NotImplemented
  
  def __gt__(self, other: Self):
    if hasattr(other, 'time_delta'):
      try:
        return self._time_delta > other.time_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __lt__(self, other: Self):
    if hasattr(other, 'time_delta'):
      try:
        return self._time_delta < other.time_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __ge__(self, other: Self):
    if hasattr(other, 'time_delta'):
      try:
        return self._time_delta >= other.time_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __le__(self, other: Self):
    if hasattr(other, 'time_delta'):
      try:
        return self._time_delta <= other.time_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
