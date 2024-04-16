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
  
  def __neg__(self) -> Self:
    return DateDelta(-self._date_delta)
  
  def __add__(self, other: Self) -> Self:
    return DateDelta(self._date_delta + other._date_delta)
  
  def __sub__(self, other: Self) -> Self:
    return self + (-other)
  
  def __mul__(self, other) -> Self:
    return DateDelta(self._date_delta * other)
  
  def __floordiv__(self, other) -> Self:
    return DateDelta(self._date_delta // other)
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    return self._date_delta == other._date_delta
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    return self._date_delta != other._date_delta
  
  def __gt__(self, other: Self):
    return self._date_delta > other._date_delta
  
  def __lt__(self, other: Self):
    return self._date_delta < other._date_delta
  
  def __ge__(self, other: Self):
    return self._date_delta >= other._date_delta
  
  def __le__(self, other: Self):
    return self._date_delta <= other._date_delta
