from datetime import timedelta
from typing import Self

from ..constants import NOMINAL_MICROSECS_PER_SEC as _NOMINAL_MICROSECS_PER_SEC
from ..constants import NOMINAL_MICROSECS_PER_DAY as _NOMINAL_MICROSECS_PER_DAY
from ..constants import NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX as _NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX
from ..fixed_prec import FixedPrec
from .lib import TimeStorageType

class TimeDelta:
  'Class representing the difference between two times, stored using the TAI length of second.'
  
  # static stuff
  
  NOMINAL_MICROSECS_PER_SEC = _NOMINAL_MICROSECS_PER_SEC
  NOMINAL_MICROSECS_PER_DAY = _NOMINAL_MICROSECS_PER_DAY
  NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX = _NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX
  
  # instance stuff
  
  __slots__ = '_time_delta'
  _time_delta: TimeStorageType
  
  def __init__(self, time_delta: FixedPrec | int | float | str | timedelta, coerce_to_fixed_prec: bool = True):
    if isinstance(time_delta, timedelta):
      time_delta = self.from_datetime_timedelta(time_delta)._time_delta
    elif coerce_to_fixed_prec and not isinstance(time_delta, FixedPrec):
      time_delta = FixedPrec.from_basic(time_delta)
    
    self._time_delta = time_delta
  
  @classmethod
  def from_datetime_timedelta(cls, timedelta_obj: timedelta) -> Self:
    total_microseconds = timedelta_obj.days * cls.NOMINAL_MICROSECS_PER_DAY + \
      timedelta_obj.seconds * cls.NOMINAL_MICROSECS_PER_SEC + \
      timedelta_obj.microseconds
    
    return cls(FixedPrec(total_microseconds, cls.NOMINAL_MICROSECS_PER_SEC_LOG_FIXEDPREC_RADIX))
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self._time_delta!r})'
  
  def __str__(self) -> str:
    return f'TD{self._time_delta:+}'
  
  @property
  def time_delta(self) -> TimeStorageType:
    return self._time_delta
  
  def to_hashable_tuple(self) -> tuple[str, TimeStorageType]:
    return ('TimeDelta', self._time_delta)
  
  def __hash__(self):
    return hash(self.to_hashable_tuple())
  
  def __neg__(self) -> Self:
    try:
      return self.__class__(-self._time_delta)
    except TypeError:
      return NotImplemented
  
  def __pos__(self) -> Self:
    return self
  
  def __abs__(self) -> Self:
    try:
      if self._time_delta < 0:
        return -self
      else:
        return self
    except TypeError:
      return NotImplemented
  
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
      try:
        return self.time_delta / other.time_delta
      except TypeError:
        return NotImplemented
    else:
      try:
        return self.__class__(self._time_delta / other)
      except TypeError:
        return NotImplemented
  
  def __floordiv__(self, other) -> int:
    if hasattr(other, 'time_delta'):
      try:
        return int(self.time_delta // other.time_delta)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __mod__(self, other) -> Self:
    if hasattr(other, 'time_delta'):
      try:
        return self.__class__(self.time_delta % other.time_delta)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __divmod__(self, other) -> tuple[int, Self]:
    if hasattr(other, 'time_delta'):
      try:
        whole, remainder = divmod(self.time_delta, other.time_delta)
        return int(whole), self.__class__(remainder)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __radd__(self, other: Self) -> Self:
    if hasattr(other, 'time_delta'):
      try:
        return self.__class__(other.time_delta + self._time_delta)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __rsub__(self, other: Self) -> Self:
    try:
      return (-self) + other
    except TypeError:
      return NotImplemented
  
  def __rmul__(self, other) -> Self:
    if hasattr(other, 'time_delta'):
      return NotImplemented
    else:
      try:
        return self.__class__(other * self._time_delta)
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
  
  def to_datetime_timedelta(self) -> timedelta:
    return timedelta(microseconds = int(self._time_delta * self.NOMINAL_MICROSECS_PER_SEC))
