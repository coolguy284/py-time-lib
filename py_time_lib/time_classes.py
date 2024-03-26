from .fixed_prec import FixedPrec

class TimeDelta:
  __slots__ = '_time_delta'
  
  def __init__(self, time_delta, coerce_to_fixed_prec = True):
    if coerce_to_fixed_prec and not isinstance(time_delta, FixedPrec):
      time_delta = FixedPrec.from_any(time_delta)
    
    self._time_delta = time_delta
  
  def __repr__(self):
    return f'{self.__class__.__name__}({self._time_delta!r})'
  
  def __str__(self):
    return f'TD{self._time_delta:+}'
  
  def __neg__(self):
    return TimeDelta(-self._time_delta)
  
  def __add__(self, other):
    return TimeDelta(self._time_delta + other._time_delta)
  
  def __sub__(self, other):
    return self + (-other)
  
  def __mul__(self, other):
    return TimeDelta(self._time_delta * other)
  
  def __truediv__(self, other):
    return TimeDelta(self._time_delta / other)
  
  def __eq__(self, other):
    return self._time_delta == other._time_delta
  
  def __ne__(self, other):
    return self._time_delta != other._time_delta
  
  def __gt__(self, other):
    return self._time_delta > other._time_delta
  
  def __lt__(self, other):
    return self._time_delta < other._time_delta
  
  def __ge__(self, other):
    return self._time_delta >= other._time_delta
  
  def __le__(self, other):
    return self._time_delta <= other._time_delta

class TimeInstant:
  __slots__ = '_time'
  
  def __init__(self, time, coerce_to_fixed_prec = True):
    if coerce_to_fixed_prec and not isinstance(time, FixedPrec):
      time = FixedPrec.from_any(time)
    
    self._time = time
  
  def __repr__(self):
    return f'{self.__class__.__name__}({self._time!r})'
  
  def __str__(self):
    return f'T{self._time:+}'
  
  def __add__(self, other):
    return TimeInstant(self._time + other._time_delta)
  
  def __sub__(self, other):
    if hasattr(other, '_time'):
      return TimeDelta(self._time - other._time)
    else:
      return TimeInstant(self._time - other._time_delta)
  
  def __eq__(self, other):
    return self._time == other._time
  
  def __ne__(self, other):
    return self._time != other._time
  
  def __gt__(self, other):
    return self._time > other._time
  
  def __lt__(self, other):
    return self._time < other._time
  
  def __ge__(self, other):
    return self._time >= other._time
  
  def __le__(self, other):
    return self._time <= other._time
