from .lib_funcs import binary_search, binary_search_array_split
from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate
from .data.leap_seconds import LEAP_SECONDS as DATA_LEAP_SECONDS

class TimeDelta:
  __slots__ = '_time_delta'
  
  def __init__(self, time_delta, coerce_to_fixed_prec = True):
    if coerce_to_fixed_prec and not isinstance(time_delta, FixedPrec):
      time_delta = FixedPrec.from_basic(time_delta)
    
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
  
  NOMINAL_SECS_PER_DAY = 86_400
  NOMINAL_SECS_PER_HOUR = 3_600
  NOMINAL_SECS_PER_MIN = 60
  
  # leap second functionality unimplemented for now
  # data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
  UTC_INITIAL_OFFSET_FROM_TAI = FixedPrec(-10, 0)
  LEAP_SECONDS = DATA_LEAP_SECONDS
  
  @classmethod
  def _init_class_vars(cls):
    leap_secs = [(GregorianDate.from_iso_string(date_string).to_days_since_epoch() + 1, utc_delta) for date_string, utc_delta in cls.LEAP_SECONDS]
    pre_epoch_leap_secs, _ = binary_search_array_split(leap_secs, lambda x: x[0] < 0)
    pre_epoch_leap_secs.reverse()
    
    current_utc_tai_offset = cls.UTC_INITIAL_OFFSET_FROM_TAI
    cls.TAI_TO_UTC_OFFSET_TABLE = [
      # format:
      # [FixedPrec time instant, positive_leap_second_occurring, utc_tai_delta | utc_epoch_secs, leap_utc_delta]
      # applies when time is after or equal to this time instant
      # if a positive leap second is occurring, the fixed utc epoch seconds value is given
      # otherwise, the utc-tai delta is given
    ]
    
    for leap_entry in leap_secs:
      days_since_epoch, utc_delta = leap_entry
      leap_sec_base_time_utc = FixedPrec.from_basic(days_since_epoch * cls.NOMINAL_SECS_PER_DAY)
      leap_sec_base_time = FixedPrec.from_basic(leap_sec_base_time_utc - current_utc_tai_offset)
      if utc_delta < 0:
        # "positive" leap second (utc clocks are paused for one second; 11:59:59 PM UTC -> 11:59:60 PM UTC -> 12:00:00 AM UTC)
        current_utc_tai_offset += utc_delta
        cls.TAI_TO_UTC_OFFSET_TABLE.append([leap_sec_base_time, True, leap_sec_base_time_utc, utc_delta])
        cls.TAI_TO_UTC_OFFSET_TABLE.append([leap_sec_base_time - utc_delta, False, current_utc_tai_offset, utc_delta])
      elif utc_delta > 0:
        # "negative" leap second (utc clocks skip one second; 11:59:58 PM UTC -> 12:00:00 AM UTC)
        current_utc_tai_offset += utc_delta
        cls.TAI_TO_UTC_OFFSET_TABLE.append([leap_sec_base_time - utc_delta, False, current_utc_tai_offset, utc_delta])
  
  def __init__(self, time, coerce_to_fixed_prec = True):
    if coerce_to_fixed_prec and not isinstance(time, FixedPrec):
      time = FixedPrec.from_basic(time)
    
    self._time = time
  
  def __repr__(self):
    return f'{self.__class__.__name__}({self._time!r})'
  
  def __str__(self):
    return f'T{self._time:+}'
  
  @property
  def time(self):
    return self._time
  
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
  
  def to_gregorian_date_tuple_tai(self):
    'Returns a gregorian date tuple in the TAI timezone (as math is easiest for this).'
    days_since_epoch = self._time // self.NOMINAL_SECS_PER_DAY
    time_since_day_start = self._time - days_since_epoch * self.NOMINAL_SECS_PER_DAY
    date = GregorianDate.from_days_since_epoch(days_since_epoch)
    hour, remainder = divmod(time_since_day_start, self.NOMINAL_SECS_PER_HOUR)
    minute, remainder = divmod(remainder, self.NOMINAL_SECS_PER_MIN)
    second, frac_second = divmod(remainder, 1)
    return date.year, date.month, date.day, int(hour), int(minute), int(second), frac_second
  
  def to_utc_info(self):
    'Returns a dict of the form (utc_seconds_since_epoch, positive_leap_second_occurring, time_since_positive_leap_second_start).'
    if len(self.TAI_TO_UTC_OFFSET_TABLE) == 0:
      return {
        'utc_seconds_since_epoch': self._time + self.UTC_INITIAL_OFFSET_FROM_TAI,
        'positive_leap_second_occurring': False,
        'last_leap_delta': None,
        'time_since_last_leap_second_start': None,
      }
    else:
      if self._time < self.TAI_TO_UTC_OFFSET_TABLE[0][0]:
        return {
          'utc_seconds_since_epoch': self._time + self.UTC_INITIAL_OFFSET_FROM_TAI,
          'positive_leap_second_occurring': False,
          'last_leap_delta': None,
          'time_since_last_leap_second_start': None,
        }
      else:
        tai_table_index = binary_search(lambda x: self._time > self.TAI_TO_UTC_OFFSET_TABLE[x][0], 0, len(self.TAI_TO_UTC_OFFSET_TABLE))
        start_instant, positive_leap_second_occurring, utc_data, utc_delta = self.TAI_TO_UTC_OFFSET_TABLE[tai_table_index]
        if positive_leap_second_occurring:
          utc_epoch_secs = utc_data
          return {
            'utc_seconds_since_epoch': utc_epoch_secs,
            'positive_leap_second_occurring': True,
            'last_leap_delta': utc_delta,
            'time_since_last_leap_second_start': self._time - start_instant,
          }
        else:
          utc_tai_delta = utc_data
          return {
            'utc_seconds_since_epoch': self._time + utc_tai_delta,
            'positive_leap_second_occurring': False,
            'last_leap_delta': utc_delta,
            'time_since_last_leap_second_start': self._time - start_instant,
          }
  
  def to_utc_secs_since_epoch(self):
    'Returns a tuple of the form (utc_seconds_since_epoch, second_fold). For a leap second, the counter goes back one second, and fold gets set to true.'
    utc_info = self.to_utc_info()
    utc_seconds_since_epoch = utc_info['utc_seconds_since_epoch']
    positive_leap_second_occurring = utc_info['positive_leap_second_occurring']
    last_leap_delta = utc_info['last_leap_delta']
    time_since_last_leap_second_start = utc_info['time_since_last_leap_second_start']
    # TODO fix implementation, but can only be done if there is a way to know if you are one second after a positive leap second finished
    if not positive_leap_second_occurring:
      if last_leap_delta < 0 and time_since_last_leap_second_start < 2 * -last_leap_delta:
        # last leap second was a positive leap second and folds are necessary
        return utc_seconds_since_epoch, True
      else:
        # last leap second was a negative leap second, no folds necessary
        return utc_seconds_since_epoch, False
    else:
      return utc_seconds_since_epoch + time_since_last_leap_second_start, False

TimeInstant._init_class_vars()
