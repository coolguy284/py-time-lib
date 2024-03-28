from .lib_funcs import binary_search_array_split
from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate
from .data.leap_seconds import LEAP_SECONDS as DATA_LEAP_SECONDS

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
  LEAP_SECONDS = DATA_LEAP_SECONDS
  
  @classmethod
  def _init_class_vars(cls):
    leap_secs_epoch_days = [(GregorianDate.from_iso_string(date_string).to_days_since_epoch(), utc_delta) for date_string, utc_delta in cls.LEAP_SECONDS]
    pre_epoch_leap_secs, after_or_during_epoch_leap_secs = binary_search_array_split(leap_secs_epoch_days, lambda x: x[0] < 0)
    pre_epoch_leap_secs.reverse()
    print([pre_epoch_leap_secs, after_or_during_epoch_leap_secs])
  
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

TimeInstant._init_class_vars()
