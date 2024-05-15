from abc import abstractmethod
from numbers import Integral

from .date_base import DateBase

class YearlyCalendarBase(DateBase):
  'Adds functions for calendars that follow a yearly cycle.'
  
  # static stuff
  
  # instance stuff
  
  __slots__ = '_year'
  _year: Integral
  
  @property
  def year(self) -> Integral:
    return self._year

class ThreeTupleBase(YearlyCalendarBase):
  'Adds functions for calendars whose dates are a three-tuple of (year, something, something).'
  
  # static stuff
  
  @classmethod
  @abstractmethod
  def date_to_days_since_epoch[T: Integral](cls, *date: tuple[T, T, T]) -> T:
    ...
  
  @classmethod
  @abstractmethod
  def days_since_epoch_to_date[T: Integral](cls, days_since_epoch: T) -> tuple[T, T, T]:
    ...
  
  # instance stuff
  
  __slots__ = ()
  
  @abstractmethod
  def to_date_tuple[T: Integral](self) -> tuple[T, T, T]:
    ...
  
  def ordinal_date(self) -> int:
    return self.days_since_epoch - self.__class__(self.year, 1, 1).days_since_epoch + 1
