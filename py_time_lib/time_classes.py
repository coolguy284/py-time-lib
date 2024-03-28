from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate

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
  '''Class representing an instant of time. Modeled after TAI, with epoch at jan 1, 1 BCE (year 0). Stores seconds since epoch.'''
  
  __slots__ = '_time'
  
  # leap second functionality unimplemented for now
  # data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
  UTC_INITIAL_OFFSET_FROM_TAI = FixedPrec(-10, 0)
  LEAP_SECONDS = [
    # [date, utc delta]
    ['1972-06-30', FixedPrec(-1, 0)],
    ['1972-12-31', FixedPrec(-1, 0)],
    ['1973-12-31', FixedPrec(-1, 0)],
    ['1974-12-31', FixedPrec(-1, 0)],
    ['1975-12-31', FixedPrec(-1, 0)],
    ['1976-12-31', FixedPrec(-1, 0)],
    ['1977-12-31', FixedPrec(-1, 0)],
    ['1978-12-31', FixedPrec(-1, 0)],
    ['1979-12-31', FixedPrec(-1, 0)],
    ['1981-06-30', FixedPrec(-1, 0)],
    ['1982-06-30', FixedPrec(-1, 0)],
    ['1983-06-30', FixedPrec(-1, 0)],
    ['1985-06-30', FixedPrec(-1, 0)],
    ['1987-12-31', FixedPrec(-1, 0)],
    ['1989-12-31', FixedPrec(-1, 0)],
    ['1990-12-31', FixedPrec(-1, 0)],
    ['1992-06-30', FixedPrec(-1, 0)],
    ['1993-06-30', FixedPrec(-1, 0)],
    ['1994-06-30', FixedPrec(-1, 0)],
    ['1995-12-31', FixedPrec(-1, 0)],
    ['1997-06-30', FixedPrec(-1, 0)],
    ['1998-12-31', FixedPrec(-1, 0)],
    ['2005-12-31', FixedPrec(-1, 0)],
    ['2008-12-31', FixedPrec(-1, 0)],
    ['2012-06-30', FixedPrec(-1, 0)],
    ['2015-06-30', FixedPrec(-1, 0)],
    ['2016-12-31', FixedPrec(-1, 0)],
  ]
  
  @classmethod
  def _init_class_vars(cls):
    ...
  
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
