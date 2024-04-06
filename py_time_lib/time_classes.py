from contextlib import contextmanager
from numbers import Integral, Real
from typing import Generator, Self, SupportsIndex

from .lib_funcs import binary_search
from .fixed_prec import FixedPrec
from .calendars.gregorian import GregorianDate
from .calendars.jul_greg_base import JulGregBaseDate
from .data.leap_seconds import LEAP_SECONDS as DATA_LEAP_SECONDS

class TimeDelta:
  'Class representing the difference between two times, stored using the TAI length of second.'
  
  __slots__ = '_time_delta'
  _time_delta: FixedPrec | Real
  
  def __init__(self, time_delta: FixedPrec | int | float | str, coerce_to_fixed_prec: bool = True):
    if coerce_to_fixed_prec and not isinstance(time_delta, FixedPrec):
      time_delta = FixedPrec.from_basic(time_delta)
    
    self._time_delta = time_delta
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self._time_delta!r})'
  
  def __str__(self) -> str:
    return f'TD{self._time_delta:+}'
  
  def __neg__(self) -> Self:
    return TimeDelta(-self._time_delta)
  
  def __add__(self, other: Self) -> Self:
    return TimeDelta(self._time_delta + other._time_delta)
  
  def __sub__(self, other: Self) -> Self:
    return self + (-other)
  
  def __mul__(self, other) -> Self:
    return TimeDelta(self._time_delta * other)
  
  def __truediv__(self, other) -> Self:
    return TimeDelta(self._time_delta / other)
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    return self._time_delta == other._time_delta
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    return self._time_delta != other._time_delta
  
  def __gt__(self, other: Self):
    return self._time_delta > other._time_delta
  
  def __lt__(self, other: Self):
    return self._time_delta < other._time_delta
  
  def __ge__(self, other: Self):
    return self._time_delta >= other._time_delta
  
  def __le__(self, other: Self):
    return self._time_delta <= other._time_delta

class TimeInstant:
  'Class representing an instant of time. Modeled after TAI, with epoch at jan 1, 1 BCE (year 0). Stores seconds since epoch.'
  
  # static stuff
  
  NOMINAL_SECS_PER_DAY = 86_400
  NOMINAL_SECS_PER_HOUR = 3_600
  NOMINAL_SECS_PER_MIN = 60
  
  # data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
  UTC_INITIAL_OFFSET_FROM_TAI = FixedPrec(-10, 0)
  LEAP_SECONDS = DATA_LEAP_SECONDS
  
  @classmethod
  def epoch_instant_to_date_tuple(cls, secs_since_epoch: FixedPrec, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, FixedPrec | Real]:
    days_since_epoch, time_since_day_start = divmod(secs_since_epoch, cls.NOMINAL_SECS_PER_DAY)
    date = date_cls.from_days_since_epoch(int(days_since_epoch))
    hour, remainder = divmod(time_since_day_start, cls.NOMINAL_SECS_PER_HOUR)
    minute, remainder = divmod(remainder, cls.NOMINAL_SECS_PER_MIN)
    second, frac_second = divmod(remainder, 1)
    return *date.to_date_tuple(), int(hour), int(minute), int(second), frac_second
  
  @classmethod
  def _init_class_vars(cls) -> None:
    leap_secs = []
    for date_string, time_in_day, utc_delta in cls.LEAP_SECONDS:
      days_since_epoch = GregorianDate.from_iso_string(date_string).to_days_since_epoch()
      days_since_epoch_delt, time_in_day = divmod(time_in_day, cls.NOMINAL_SECS_PER_DAY)
      leap_secs.append({
        'days_since_epoch': int(days_since_epoch + days_since_epoch_delt),
        'time_in_day': time_in_day,
        'utc_delta': utc_delta,
      })
    
    leap_secs_dict_working = {}
    
    for leap_entry_dict in leap_secs:
      if leap_entry_dict['days_since_epoch'] not in leap_secs_dict_working:
        leap_secs_dict_working[leap_entry_dict['days_since_epoch']] = [leap_entry_dict]
      else:
        leap_secs_dict_working[leap_entry_dict['days_since_epoch']].append(leap_entry_dict)
    
    # https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops/3294899#3294899
    cls.LEAP_SECONDS_DICT: dict[int, tuple[dict[str, int | FixedPrec], ...]] = dict([(day, tuple(leap_entries)) for day, leap_entries in leap_secs_dict_working.items()])
    
    current_utc_tai_offset = cls.UTC_INITIAL_OFFSET_FROM_TAI
    
    cls.TAI_TO_UTC_OFFSET_TABLE: dict[str, FixedPrec | bool | None] = [
      # format:
      # { start_instant: FixedPrec (TAI), positive_leap_second_occurring, utc_tai_delta | utc_epoch_secs, leap_utc_delta }
      # applies when time is after or equal to this time instant
      # if a positive leap second is occurring, the fixed utc epoch seconds value is given
      # otherwise, the utc-tai delta is given
    ]
    
    cls.UTC_TO_TAI_OFFSET_TABLE = [
      # format:
      # { start_instant: FixedPrec (UTC), utc_tai_delta: tuple(0 or more elems), leap_utc_delta }
    ]
    
    for leap_entry in leap_secs:
      leap_sec_base_time_utc = leap_entry['days_since_epoch'] * cls.NOMINAL_SECS_PER_DAY + leap_entry['time_in_day']
      leap_sec_base_time = leap_sec_base_time_utc - current_utc_tai_offset
      leap_utc_delta = leap_entry['utc_delta']
      if leap_utc_delta < 0:
        # "positive" leap second (utc clocks are paused / loop backward for one second; 11:59:59 PM UTC -> 11:59:60 PM UTC -> 12:00:00 AM UTC)
        current_utc_tai_offset += leap_utc_delta
        cls.TAI_TO_UTC_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time,
          'positive_leap_second_occurring': True,
          'utc_epoch_secs': leap_sec_base_time_utc,
          'leap_utc_delta': leap_utc_delta,
        })
        cls.TAI_TO_UTC_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time - leap_utc_delta,
          'positive_leap_second_occurring': False,
          'utc_tai_delta': current_utc_tai_offset,
          'leap_utc_delta': leap_utc_delta,
        })
        cls.UTC_TO_TAI_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time_utc,
          'utc_tai_delta': (current_utc_tai_offset - leap_utc_delta, current_utc_tai_offset),
          'leap_utc_delta': leap_utc_delta,
        })
        cls.UTC_TO_TAI_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time_utc - leap_utc_delta,
          'utc_tai_delta': (current_utc_tai_offset,),
          'leap_utc_delta': leap_utc_delta,
        })
      elif leap_utc_delta > 0:
        # "negative" leap second (utc clocks skip one second; 11:59:58 PM UTC -> 12:00:00 AM UTC)
        current_utc_tai_offset += leap_utc_delta
        cls.TAI_TO_UTC_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time - leap_utc_delta,
          'positive_leap_second_occurring': False,
          'utc_tai_delta': current_utc_tai_offset,
          'leap_utc_delta': leap_utc_delta,
        })
        cls.UTC_TO_TAI_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time_utc - leap_utc_delta,
          'utc_tai_delta': (),
          'leap_utc_delta': leap_utc_delta,
        })
        cls.UTC_TO_TAI_OFFSET_TABLE.append({
          'start_instant': leap_sec_base_time_utc,
          'utc_tai_delta': (current_utc_tai_offset,),
          'leap_utc_delta': leap_utc_delta,
        })
  
  @classmethod
  @contextmanager
  def _auto_reset_class_vars(cls) -> Generator[None, None, None]:
    'Automatically resets UTC_INITIAL_OFFSET_FROM_TAI, LEAP_SECONDS, and NOMINAL_SECS_PER_DAY after exiting the context block.'
    UTC_INITIAL_OFFSET_FROM_TAI = cls.UTC_INITIAL_OFFSET_FROM_TAI
    NOMINAL_SECS_PER_DAY = cls.NOMINAL_SECS_PER_DAY
    LEAP_SECONDS = cls.LEAP_SECONDS[:]
    
    try:
      yield
    finally:
      cls.UTC_INITIAL_OFFSET_FROM_TAI = UTC_INITIAL_OFFSET_FROM_TAI
      cls.NOMINAL_SECS_PER_DAY = NOMINAL_SECS_PER_DAY
      cls.LEAP_SECONDS.clear()
      cls.LEAP_SECONDS.extend(LEAP_SECONDS)
      cls._init_class_vars()
  
  @classmethod
  @contextmanager
  def _temp_add_leap_sec(cls, position: SupportsIndex, leap_entry: tuple[str, FixedPrec]) -> Generator[None, None, None]:
    # https://stackoverflow.com/questions/8720179/nesting-python-context-managers/8720431#8720431
    with cls._auto_reset_class_vars():
      TimeInstant.LEAP_SECONDS.insert(position, leap_entry)
      TimeInstant._init_class_vars()
      
      try:
        yield
      finally:
        pass
  
  @classmethod
  @contextmanager
  def _temp_add_leap_secs(cls, position: SupportsIndex, leap_entries: list[tuple[str, FixedPrec]]) -> Generator[None, None, None]:
    # https://stackoverflow.com/questions/8720179/nesting-python-context-managers/8720431#8720431
    with cls._auto_reset_class_vars():
      TimeInstant.LEAP_SECONDS[position:position] = leap_entries
      TimeInstant._init_class_vars()
      
      try:
        yield
      finally:
        pass
  
  @classmethod
  def from_utc_secs_since_epoch(cls, utc_seconds_since_epoch: Integral, second_fold: bool = False, round_invalid_time_upwards: bool = True) -> Self:
    if len(cls.UTC_TO_TAI_OFFSET_TABLE) == 0:
      return cls(utc_seconds_since_epoch - cls.UTC_INITIAL_OFFSET_FROM_TAI)
    else:
      if utc_seconds_since_epoch < cls.UTC_TO_TAI_OFFSET_TABLE[0]['start_instant']:
        return cls(utc_seconds_since_epoch - cls.UTC_INITIAL_OFFSET_FROM_TAI)
      else:
        utc_table_index = binary_search(lambda x: utc_seconds_since_epoch >= cls.UTC_TO_TAI_OFFSET_TABLE[x]['start_instant'], 0, len(cls.UTC_TO_TAI_OFFSET_TABLE))
        utc_table_entry = cls.UTC_TO_TAI_OFFSET_TABLE[utc_table_index]
        if len(utc_table_entry['utc_tai_delta']) == 0:
          # time cannot map to tai, but can round up
          if round_invalid_time_upwards:
            utc_table_next_entry = cls.UTC_TO_TAI_OFFSET_TABLE[utc_table_index + 1]
            return cls(utc_table_entry['start_instant'] - (utc_table_next_entry['utc_tai_delta'][0] - utc_table_entry['leap_utc_delta']))
          else:
            raise Exception('utc time does not map to tai')
        elif len(utc_table_entry['utc_tai_delta']) == 1:
          return cls(utc_seconds_since_epoch - utc_table_entry['utc_tai_delta'][0])
        else:
          if second_fold:
            return cls(utc_seconds_since_epoch - utc_table_entry['utc_tai_delta'][1])
          else:
            return cls(utc_seconds_since_epoch - utc_table_entry['utc_tai_delta'][0])
  
  @classmethod
  def from_date_tuple_tai(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: FixedPrec | Real, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a tai TimeInstant.'
    date = date_cls(year, month, day)
    time = date.to_days_since_epoch() * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    return TimeInstant(time)
  
  @classmethod
  def from_date_tuple_utc(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: FixedPrec | Real, round_invalid_time_upwards: bool = True, date_cls: type[JulGregBaseDate] = GregorianDate) -> Self:
    'Converts a tuple of the form (year, month, day, hour, minute, second, frac_second) into a utc TimeInstant. Does not handle leap seconds that occur during the day.'
    date = date_cls(year, month, day)
    time = date.to_days_since_epoch() * cls.NOMINAL_SECS_PER_DAY
    time += hour * cls.NOMINAL_SECS_PER_HOUR
    time += minute * cls.NOMINAL_SECS_PER_MIN
    time += second
    time += frac_second
    date_days = date.to_days_since_epoch()
    if date_days in cls.LEAP_SECONDS_DICT:
      leap_entries = cls.LEAP_SECONDS_DICT[date_days]
      leap_delta = leap_entries[-1]['utc_delta']
      if leap_delta < 0:
        # positive leap second
        if hour * cls.NOMINAL_SECS_PER_HOUR + minute * cls.NOMINAL_SECS_PER_MIN + second + frac_second < -leap_delta:
          leap_fold = True
        else:
          leap_fold = False
      else:
        leap_fold = False
    else:
      leap_fold = False
    return TimeInstant.from_utc_secs_since_epoch(time, second_fold = leap_fold, round_invalid_time_upwards = round_invalid_time_upwards)
  
  # instance stuff
  
  __slots__ = '_time'
  _time: FixedPrec | Real
  
  def __init__(self, time: FixedPrec | int | float | str, coerce_to_fixed_prec: bool = True):
    if coerce_to_fixed_prec and not isinstance(time, FixedPrec):
      time = FixedPrec.from_basic(time)
    
    self._time = time
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}({self._time!r})'
  
  def __str__(self) -> str:
    return f'T{self._time:+}'
  
  @property
  def time(self) -> FixedPrec | Real:
    return self._time
  
  def __add__(self, other: TimeDelta) -> Self:
    return TimeInstant(self._time + other._time_delta)
  
  def __sub__(self, other: Self | TimeDelta) -> Self | TimeDelta:
    if hasattr(other, '_time'):
      return TimeDelta(self._time - other._time)
    else:
      return TimeInstant(self._time - other._time_delta)
  
  def __eq__(self, other: Self | None):
    if other is None:
      return False
    
    return self._time == other._time
  
  def __ne__(self, other: Self | None):
    if other is None:
      return True
    
    return self._time != other._time
  
  def __gt__(self, other: Self):
    return self._time > other._time
  
  def __lt__(self, other: Self):
    return self._time < other._time
  
  def __ge__(self, other: Self):
    return self._time >= other._time
  
  def __le__(self, other: Self):
    return self._time <= other._time
  
  def to_utc_info(self) -> dict[str, FixedPrec | Real | bool | None]:
    'Returns a dict of the form (utc_seconds_since_epoch, positive_leap_second_occurring, last_leap_delta, last_leap_transition_time (when last leap second started or ended)).'
    if len(self.TAI_TO_UTC_OFFSET_TABLE) == 0:
      return {
        'utc_seconds_since_epoch': self._time + self.UTC_INITIAL_OFFSET_FROM_TAI,
        'positive_leap_second_occurring': False,
        'last_leap_delta': None,
        'last_leap_transition_time': None,
      }
    else:
      if self._time < self.TAI_TO_UTC_OFFSET_TABLE[0]['start_instant']:
        return {
          'utc_seconds_since_epoch': self._time + self.UTC_INITIAL_OFFSET_FROM_TAI,
          'positive_leap_second_occurring': False,
          'last_leap_delta': None,
          'last_leap_transition_time': None,
        }
      else:
        tai_table_index = binary_search(lambda x: self._time >= self.TAI_TO_UTC_OFFSET_TABLE[x]['start_instant'], 0, len(self.TAI_TO_UTC_OFFSET_TABLE))
        tai_table_entry = self.TAI_TO_UTC_OFFSET_TABLE[tai_table_index]
        if tai_table_entry['positive_leap_second_occurring']:
          return {
            'utc_seconds_since_epoch': tai_table_entry['utc_epoch_secs'],
            'positive_leap_second_occurring': True,
            'last_leap_delta': tai_table_entry['leap_utc_delta'],
            'last_leap_transition_time': tai_table_entry['start_instant'],
          }
        else:
          return {
            'utc_seconds_since_epoch': self._time + tai_table_entry['utc_tai_delta'],
            'positive_leap_second_occurring': False,
            'last_leap_delta': tai_table_entry['leap_utc_delta'],
            'last_leap_transition_time': tai_table_entry['start_instant'],
          }
  
  def to_utc_secs_since_epoch(self) -> tuple[FixedPrec | Real, bool]:
    'Returns a tuple of the form (utc_seconds_since_epoch, second_fold). For a leap second, the counter goes back one second, and fold gets set to true.'
    utc_info = self.to_utc_info()
    utc_seconds_since_epoch = utc_info['utc_seconds_since_epoch']
    positive_leap_second_occurring = utc_info['positive_leap_second_occurring']
    last_leap_delta = utc_info['last_leap_delta']
    last_leap_transition_time = utc_info['last_leap_transition_time']
    # TODO fix implementation, but can only be done if there is a way to know if you are one second after a positive leap second finished
    if not positive_leap_second_occurring:
      if last_leap_delta != None:
        if last_leap_delta < 0 and self.time - last_leap_transition_time < -last_leap_delta:
          # last leap second was a positive leap second and folds are necessary
          return utc_seconds_since_epoch, True
        else:
          # last leap second was a negative leap second, no folds necessary
          return utc_seconds_since_epoch, False
      else:
        return utc_seconds_since_epoch, False
    else:
      return utc_seconds_since_epoch + (self.time - last_leap_transition_time), False
  
  def to_date_tuple_tai(self, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, FixedPrec | Real]:
    'Returns a date tuple in the TAI timezone (as math is easiest for this).'
    return self.epoch_instant_to_date_tuple(self._time, date_cls = date_cls)
  
  def to_date_tuple_utc(self, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[Integral, Integral, Integral, int, int, int, FixedPrec | Real]:
    'Returns a date tuple in the UTC timezone. Does not handle leap seconds that occur during the day.'
    utc_info = self.to_utc_info()
    utc_secs_since_epoch = utc_info['utc_seconds_since_epoch']
    if utc_info['positive_leap_second_occurring']:
      utc_secs_since_epoch -= 1
    *date, hour, minute, second, frac_second = self.epoch_instant_to_date_tuple(utc_secs_since_epoch, date_cls = date_cls)
    if utc_info['positive_leap_second_occurring']:
      second += 1
      second_addl, frac_second = divmod(frac_second + (self._time - utc_info['last_leap_transition_time']), 1)
      second = int(second + second_addl)
    return *date, hour, minute, second, frac_second

TimeInstant._init_class_vars()
