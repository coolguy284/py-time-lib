from contextlib import contextmanager
from typing import Generator, SupportsIndex

from ...fixed_prec import FixedPrec
from ...data import leap_seconds
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType

class TimeInstantBase:
  'TimeInstant base class. Provides basic functionality of class.'
  
  # static stuff
  
  NOMINAL_SECS_PER_DAY = leap_seconds.NOMINAL_SECS_PER_DAY
  NOMINAL_SECS_PER_HOUR = 3_600
  NOMINAL_SECS_PER_MIN = 60
  NOMINAL_MINS_PER_DAY = 1440
  NOMINAL_MINS_PER_HOUR = 60
  NOMINAL_HOURS_PER_DAY = 24
  
  # data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
  UTC_INITIAL_OFFSET_FROM_TAI = leap_seconds.UTC_INITIAL_OFFSET_FROM_TAI
  LEAP_SECONDS = leap_seconds.LEAP_SECONDS
  
  @classmethod
  def _init_class_vars(cls) -> None:
    leap_secs = []
    for date_string, time_in_day, utc_delta in cls.LEAP_SECONDS:
      days_since_epoch = GregorianDate.from_iso_string(date_string).days_since_epoch
      days_since_epoch_delt, time_in_day = divmod(time_in_day, cls.NOMINAL_SECS_PER_DAY)
      leap_secs.append({
        'days_since_epoch': int(days_since_epoch + days_since_epoch_delt),
        'time_in_day': time_in_day,
        'utc_delta': utc_delta,
      })
    
    leap_secs_dict_working = {}
    
    for leap_entry_dict in leap_secs:
      mins_in_day = cls.days_and_secs_to_mins_since_epoch(leap_entry_dict['days_since_epoch'], leap_entry_dict['time_in_day'])[0]
      if mins_in_day not in leap_secs_dict_working:
        leap_secs_dict_working[mins_in_day] = [leap_entry_dict]
      else:
        leap_secs_dict_working[mins_in_day].append(leap_entry_dict)
    
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
      cls.LEAP_SECONDS.insert(position, leap_entry)
      cls._init_class_vars()
      
      try:
        yield
      finally:
        pass
  
  @classmethod
  @contextmanager
  def _temp_add_leap_secs(cls, position: SupportsIndex, leap_entries: list[tuple[str, FixedPrec]]) -> Generator[None, None, None]:
    # https://stackoverflow.com/questions/8720179/nesting-python-context-managers/8720431#8720431
    with cls._auto_reset_class_vars():
      cls.LEAP_SECONDS[position:position] = leap_entries
      cls._init_class_vars()
      
      try:
        yield
      finally:
        pass
  
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
