from abc import abstractmethod, ABC
from numbers import Integral
from typing import Self

class DateBase(ABC):
  'Base class for all date objects. Not directly instantiated.'
  
  # static stuff
  
  @classmethod
  @abstractmethod
  def date_to_days_since_epoch[T: Integral](cls, *date: tuple[T, ...]) -> T:
    ...
  
  @classmethod
  @abstractmethod
  def days_since_epoch_to_date[T: Integral](cls, days_since_epoch: T) -> tuple[T, ...]:
    ...
  
  @classmethod
  def normalize_date[T: Integral](cls, year: T, month: T, day: T) -> tuple[T, T, T]:
    return cls.days_since_epoch_to_date(cls.date_to_days_since_epoch(year, month, day))
  
  # instance stuff
  
  __slots__ = ('_days_since_epoch',)
  _days_since_epoch: Integral
  
  # https://stackoverflow.com/questions/72644693/new-union-shorthand-giving-unsupported-operand-types-for-str-and-type/72644857#72644857
  def __init__(self, arg: tuple['str | Integral | DateBase']):
    if isinstance(arg, Integral):
      days_since_epoch = arg
      self._days_since_epoch = days_since_epoch
    elif isinstance(arg, DateBase):
      date = arg
      self._days_since_epoch = date.days_since_epoch
    else:
      raise Exception(f'Unrecognized single argument {arg!r}')
  
  @classmethod
  def from_unnormalized(cls, year: Integral, month: Integral, day: Integral) -> Self:
    'Creates a JulianDate object but accepts months and days out of range'
    return cls(*cls.normalize_date(year, month, day))
  
  @classmethod
  def from_days_since_epoch(cls, days: Integral) -> Self:
    return cls(days)
  
  @property
  def days_since_epoch(self) -> Integral:
    return self._days_since_epoch
  
  @abstractmethod
  def __repr__(self) -> str:
    ...
  
  @abstractmethod
  def __str__(self) -> str:
    ...
  
  def to_days_since_epoch(self) -> Integral:
    return self._days_since_epoch
  
  @abstractmethod
  def to_date_tuple(self) -> tuple:
    ...
  
  def add_days(self, days: Integral) -> Self:
    return self.from_days_since_epoch(self.days_since_epoch + days)
