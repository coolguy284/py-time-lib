from numbers import Integral
from typing import Self

class DateDelta:
  'Class representing the difference between two dates, stored as days.'
  
  __slots__ = '_date_delta'
  _date_delta: Integral
  
  def __init__(self, date_delta: Integral):
    self._date_delta = date_delta
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self._date_delta!r})'
  
  def __str__(self) -> str:
    return f'{self._date_delta} days'
  
  @property
  def date_delta(self) -> Integral:
    return self._date_delta
  
  def to_hashable_tuple(self) -> tuple[str, Integral]:
    return ('DateDelta', self._date_delta)
  
  def __hash__(self):
    return hash(self.to_hashable_tuple())
  
  def __neg__(self) -> Self:
    try:
      return self.__class__(-self._date_delta)
    except TypeError:
      return NotImplemented
  
  def __pos__(self) -> Self:
    return self
  
  def __abs__(self) -> Self:
    try:
      if self._date_delta < 0:
        return -self
      else:
        return self
    except TypeError:
      return NotImplemented
  
  def __add__(self, other: Self) -> Self:
    if hasattr(other, 'date_delta'):
      try:
        return self.__class__(self._date_delta + other.date_delta)
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
    if hasattr(other, 'date_delta'):
      return NotImplemented
    else:
      try:
        return self.__class__(self._date_delta * other)
      except TypeError:
        return NotImplemented
  
  def __truediv__(self, other) -> float:
    if hasattr(other, 'date_delta'):
      try:
        return self.date_delta / other.date_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __floordiv__(self, other) -> int:
    if hasattr(other, 'date_delta'):
      try:
        return int(self.date_delta // other.date_delta)
      except TypeError:
        return NotImplemented
    else:
      try:
        return self.__class__(self._date_delta // other)
      except TypeError:
        return NotImplemented
  
  def __mod__(self, other) -> Self:
    if hasattr(other, 'date_delta'):
      try:
        return self.__class__(self.date_delta % other.date_delta)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __divmod__(self, other) -> tuple[int, Self]:
    if hasattr(other, 'date_delta'):
      try:
        whole, remainder = divmod(self.date_delta, other.date_delta)
        return int(whole), self.__class__(remainder)
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __radd__(self, other: Self) -> Self:
    if hasattr(other, 'date_delta'):
      try:
        return self.__class__(other.date_delta + self._date_delta)
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
    if hasattr(other, 'date_delta'):
      return NotImplemented
    else:
      try:
        return self.__class__(other * self._date_delta)
      except TypeError:
        return NotImplemented
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    if hasattr(other, 'date_delta'):
      return self._date_delta == other.date_delta
    else:
      return NotImplemented
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    if hasattr(other, 'date_delta'):
      return self._date_delta != other.date_delta
    else:
      return NotImplemented
  
  def __gt__(self, other: Self):
    if hasattr(other, 'date_delta'):
      try:
        return self._date_delta > other.date_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __lt__(self, other: Self):
    if hasattr(other, 'date_delta'):
      try:
        return self._date_delta < other.date_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __ge__(self, other: Self):
    if hasattr(other, 'date_delta'):
      try:
        return self._date_delta >= other.date_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
  
  def __le__(self, other: Self):
    if hasattr(other, 'date_delta'):
      try:
        return self._date_delta <= other.date_delta
      except TypeError:
        return NotImplemented
    else:
      return NotImplemented
