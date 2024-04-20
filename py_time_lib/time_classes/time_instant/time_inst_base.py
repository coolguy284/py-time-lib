from ...fixed_prec import FixedPrec
from ..lib import TimeStorageType

class TimeInstantBase:
  'TimeInstant base class. Provides basic functionality of class.'
  
  # instance stuff
  
  __slots__ = '_time'
  _time: TimeStorageType
  
  def __init__(self, time: FixedPrec | int | float | str, coerce_to_fixed_prec: bool = True):
    if coerce_to_fixed_prec and not isinstance(time, FixedPrec):
      time = FixedPrec.from_basic(time)
    
    self._time = time
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self._time!r})'
  
  def __str__(self) -> str:
    return f'T{self._time:+}'
  
  @property
  def time(self) -> TimeStorageType:
    return self._time
  
  def to_hashable_tuple(self) -> tuple[str, TimeStorageType]:
    return ('TimeInstant', self._time)
  
  def __hash__(self):
    return hash(self.to_hashable_tuple())
