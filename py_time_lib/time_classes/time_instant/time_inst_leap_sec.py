from contextlib import contextmanager
from typing import Generator, Self, SupportsIndex

from ...lib_funcs import binary_search
from ...fixed_prec import FixedPrec
from ...data import leap_seconds
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType
from ..time_delta import TimeDelta
from .time_inst_ops import TimeInstantOperators

class TimeInstantLeapSec(TimeInstantOperators):
  # static stuff
  
  NOMINAL_SECS_PER_DAY = leap_seconds.NOMINAL_SECS_PER_DAY
  NOMINAL_SECS_PER_HOUR = 3_600
  NOMINAL_SECS_PER_MIN = 60
  NOMINAL_MINS_PER_DAY = 1_440
  NOMINAL_MINS_PER_HOUR = 60
  NOMINAL_HOURS_PER_DAY = 24
  NOMINAL_MICROSECS_PER_SEC = TimeDelta.NOMINAL_MICROSECS_PER_SEC
  
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
  
  __slots__ = ()
  
  @classmethod
  def from_utc_secs_since_epoch(cls, utc_seconds_since_epoch: TimeStorageType, second_fold: bool = False, round_invalid_time_upwards: bool = True) -> Self:
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
  
  def to_utc_info(self) -> dict[str, TimeStorageType | bool | None]:
    'Returns a dict of the form (utc_seconds_since_epoch, positive_leap_second_occurring, last_leap_delta, last_leap_transition_time (when last leap second started or ended)).'
    if len(self.TAI_TO_UTC_OFFSET_TABLE) == 0:
      return {
        'utc_seconds_since_epoch': self._time + self.UTC_INITIAL_OFFSET_FROM_TAI,
        'positive_leap_second_occurring': False,
        'last_leap_delta': None,
        'last_leap_transition_time': None,
        'current_utc_tai_offset': self.UTC_INITIAL_OFFSET_FROM_TAI,
      }
    else:
      if self._time < self.TAI_TO_UTC_OFFSET_TABLE[0]['start_instant']:
        return {
          'utc_seconds_since_epoch': self._time + self.UTC_INITIAL_OFFSET_FROM_TAI,
          'positive_leap_second_occurring': False,
          'last_leap_delta': None,
          'last_leap_transition_time': None,
          'current_utc_tai_offset': self.UTC_INITIAL_OFFSET_FROM_TAI,
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
            'current_utc_tai_offset': tai_table_entry['utc_epoch_secs'] - tai_table_entry['start_instant'],
          }
        else:
          return {
            'utc_seconds_since_epoch': self._time + tai_table_entry['utc_tai_delta'],
            'positive_leap_second_occurring': False,
            'last_leap_delta': tai_table_entry['leap_utc_delta'],
            'last_leap_transition_time': tai_table_entry['start_instant'],
            'current_utc_tai_offset': tai_table_entry['utc_tai_delta'],
          }
  
  def to_utc_secs_since_epoch(self) -> tuple[TimeStorageType, bool]:
    '''
    Returns a tuple of the form (utc_seconds_since_epoch, second_fold).
    After a positive leap second, the counter goes back one second,
    and fold gets set to true for one second.
    '''
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
