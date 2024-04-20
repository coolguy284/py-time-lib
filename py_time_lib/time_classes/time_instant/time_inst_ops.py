from typing import Self

from .time_inst_base import TimeInstantBase
from ..time_delta import TimeDelta

class TimeInstantOperators(TimeInstantBase):
  # instance stuff
  
  __slots__ = ()
  
  __hash__ = TimeInstantBase.__hash__
  
  def __add__(self, other: TimeDelta) -> Self:
    if hasattr(other, 'time_delta'):
      try:
        new_time = self._time + other.time_delta
      except TypeError:
        return NotImplemented
      return self.__class__(new_time)
    else:
      return NotImplemented
  
  def __sub__(self, other: Self | TimeDelta) -> Self | TimeDelta:
    if hasattr(other, 'time'):
      try:
        delta_time = self._time - other.time
      except TypeError:
        return NotImplemented
      return TimeDelta(delta_time)
    else:
      try:
        return self + (-other)
      except TypeError:
        return NotImplemented
  
  def __radd__(self, other: TimeDelta) -> Self:
    if hasattr(other, 'time_delta'):
      try:
        new_time = other.time_delta + self._time
      except TypeError:
        return NotImplemented
      return self.__class__(new_time)
    else:
      return NotImplemented
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    if hasattr(other, 'time'):
      return self._time == other.time
    else:
      return NotImplemented
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    if hasattr(other, 'time'):
      return self._time != other.time
    else:
      return NotImplemented
  
  def __gt__(self, other: Self):
    if hasattr(other, 'time'):
      try:
        return self._time > other.time
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __lt__(self, other: Self):
    if hasattr(other, 'time'):
      try:
        return self._time < other.time
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __ge__(self, other: Self):
    if hasattr(other, 'time'):
      try:
        return self._time >= other.time
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __le__(self, other: Self):
    if hasattr(other, 'time'):
      try:
        return self._time <= other.time
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
