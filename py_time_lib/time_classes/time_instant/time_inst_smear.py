from dataclasses import dataclass, field
from enum import Enum
from numbers import Integral
from typing import NamedTuple, Self
from weakref import WeakSet

from ...lib_funcs import binary_search, binary_search_float
from ...calendars.date_delta import DateDelta
from ...calendars.date_base import DateBase
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ...fixed_prec import FixedPrec
from ..lib import TimeStorageType
from ...named_tuples import DateTupleBasic, DateTupleTZ
from .time_inst_mono import TimeInstMonotonic
from ..time_zone import TimeZone

def _init_module_vars():
  global TimeInstant
  from .time_inst import TimeInstant

LeapBasis = Enum('LeapBasis', (
  'START',
  'END',
))

SmearType = Enum('SmearType', (
  'LINEAR',
  'COSINE',
))

@dataclass(frozen = True)
class LeapSmearSingle:
  start_basis: LeapBasis
  secs_before_start_basis: TimeStorageType
  end_basis: LeapBasis
  secs_after_end_basis: TimeStorageType
  type: SmearType

class LeapSmearOverrideEntry(NamedTuple):
  leap_start_tai_secs_since_epoch: TimeStorageType
  smear: LeapSmearSingle

SmearTableEntryMode = Enum('SmearTableEntryMode', (
  'FIXED_OFFSET',
  'LINEAR_SMEAR',
  'COSINE_SMEAR',
))

@dataclass(frozen = True)
class TAIToUTCSmearEntry:
  mode: SmearTableEntryMode
  tai_secs_since_epoch: TimeStorageType
  # format:
  # {
  #   if mode == 'FIXED_OFFSET':
  #     'smear_tai_offset': FixedPrec seconds,
  #   elif mode == 'LINEAR_SMEAR' or mode == 'COSINE_SMEAR':
  #     'smear_length': FixedPrec seconds,
  #     'leap_extra_secs': FixedPrec seconds,
  # }
  data: dict[str, FixedPrec]

@dataclass(frozen = True)
class UTCSmearToTAIEntry:
  mode: SmearTableEntryMode
  smear_secs_since_epoch: TimeStorageType
  # format:
  # {
  #   if mode == 'FIXED_OFFSET':
  #     'tai_smear_offset': FixedPrec seconds,
  #   elif mode == 'LINEAR_SMEAR' or mode == 'COSINE_SMEAR':
  #     'smear_length': FixedPrec seconds,
  #     'leap_extra_secs': FixedPrec seconds,
  # }
  data: dict[str, FixedPrec]

@dataclass(frozen = True)
class LeapSmearPlan():
  # static stuff
  
  @staticmethod
  def date_to_tai_start(date: GregorianDate) -> FixedPrec:
    'Returns the start time of the leap second that occured at the end of date.'
    day_after_leap = date + DateDelta(1)
    window_end_tai = TimeInstMonotonic.from_date_tuple_utc(*day_after_leap.to_date_tuple(), 0, 0, 0, 0).time
    leap_table_index = binary_search(
      lambda x: TimeInstant.TAI_TO_UTC_OFFSET_TABLE[x]['start_instant'] <= window_end_tai,
      0, len(TimeInstant.TAI_TO_UTC_OFFSET_TABLE)
    )
    leap_entry = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[leap_table_index]
    leap_instant = leap_entry['start_instant']
    if window_end_tai != leap_instant:
      raise ValueError(f'Leap second did not occur at end of {date}')
    else:
      if leap_entry['leap_utc_delta'] <= 0:
        # positive leap secoond
        past_leap_entry = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[leap_table_index - 1]
        return past_leap_entry['start_instant']
      else:
        # negative leap second
        return leap_instant
  
  # instance stuff
  
  default_smear: LeapSmearSingle
  smear_overrides: dict[FixedPrec, LeapSmearOverrideEntry]
  
  utc_smear_tai_initial_offset: TimeStorageType = field(init = False)
  tai_to_utc_smear_table: list[TAIToUTCSmearEntry] = field(init = False)
  utc_smear_to_tai_table: list[UTCSmearToTAIEntry] = field(init = False)
  
  def _generate_tables(self):
    object.__setattr__(self, 'utc_smear_tai_initial_offset', TimeInstant.UTC_INITIAL_OFFSET_FROM_TAI)
    object.__setattr__(self, 'tai_to_utc_smear_table', [])
    object.__setattr__(self, 'utc_smear_to_tai_table', [])
    
    for i in range(len(TimeInstant.TAI_TO_UTC_OFFSET_TABLE)):
      leap_entry = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[i]
      
      if leap_entry['positive_leap_second_occurring']:
        if leap_entry['start_instant'] in self.smear_overrides:
          smear_profile = self.smear_overrides[leap_entry['start_instant']]
        else:
          smear_profile = self.default_smear
        
        ...
  
  def __post_init__(self):
    self._generate_tables()
    _active_smear_plans.add(self)

_active_smear_plans: WeakSet[LeapSmearPlan] = WeakSet()

class TimeInstantLeapSmear(TimeInstMonotonic):
  # static stuff
  
  @staticmethod
  def to_linear_smear(smear_length: TimeStorageType, leap_extra_secs: TimeStorageType, tai_time_in_smear: TimeStorageType) -> TimeStorageType:
    tai_length = smear_length + leap_extra_secs
    
    if not (0 <= tai_time_in_smear <= tai_length):
      raise ValueError(f'Tai time out of range: 0 <= tai_time <= {tai_length}; tai_time is {tai_time_in_smear}')
    
    return tai_time_in_smear * smear_length / tai_length
  
  @staticmethod
  def from_linear_smear(smear_length: TimeStorageType, leap_extra_secs: TimeStorageType, smear_time_in_smear: TimeStorageType) -> TimeStorageType:
    if not (0 <= smear_time_in_smear <= smear_length):
      raise ValueError(f'Tai time out of range: 0 <= smear_time <= {smear_length}; smear_time is {smear_time_in_smear}')
    
    tai_length = smear_length + leap_extra_secs
    
    return smear_time_in_smear * tai_length / smear_length
  
  @staticmethod
  def to_cosine_smear(smear_length: TimeStorageType, leap_extra_secs: TimeStorageType, tai_time_in_smear: TimeStorageType) -> FixedPrec:
    tai_time_in_smear = FixedPrec.from_basic(tai_time_in_smear)
    tai_length = smear_length + leap_extra_secs
    
    if not (0 <= tai_time_in_smear <= tai_length):
      raise ValueError(f'Tai time out of range: 0 <= tai_time <= {tai_length}; tai_time is {tai_time_in_smear}')
    
    if tai_time_in_smear == 0:
      return tai_time_in_smear
    elif tai_time_in_smear == tai_length:
      return tai_time_in_smear - leap_extra_secs
    else:
      return binary_search_float(lambda x: TimeInstantLeapSmear.from_cosine_smear(smear_length, leap_extra_secs, x) <= tai_time_in_smear, 0, FixedPrec.from_basic(smear_length))
  
  @staticmethod
  def from_cosine_smear(smear_length: TimeStorageType, leap_extra_secs: TimeStorageType, smear_time_in_smear: TimeStorageType) -> FixedPrec:
    if not (0 <= smear_time_in_smear <= smear_length):
      raise ValueError(f'Tai time out of range: 0 <= smear_time <= {smear_length}; smear_time is {smear_time_in_smear}')
    
    smear_time_in_smear = FixedPrec.from_basic(smear_time_in_smear)
    # https://googleblog.blogspot.com/2011/09/time-technology-and-leaping-seconds.html
    half_leap_time = leap_extra_secs / 2
    
    if smear_time_in_smear == 0:
      return smear_time_in_smear
    elif smear_time_in_smear == smear_length:
      return smear_time_in_smear + leap_extra_secs
    else:
      return half_leap_time - half_leap_time * (smear_time_in_smear.pi() * smear_time_in_smear / smear_length).cos() + smear_time_in_smear
  
  # instance stuff
  
  __slots__ = ()
  
  # > utc
  
  @classmethod
  def from_secs_since_epoch_smear_utc(cls, smear_plan: LeapSmearPlan, secs_since_epoch: TimeStorageType) -> Self:
    ...
  
  @classmethod
  def from_date_tuple_smear_utc(
    cls,
    smear_plan: LeapSmearPlan,
    year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
    date_cls: type[JulGregBaseDate] = GregorianDate
  ) -> Self:
    return cls.from_secs_since_epoch_smear_utc(
      smear_plan,
      cls.date_tuple_to_epoch_instant(year, month, day, hour, minute, second, frac_second, date_cls = date_cls)
    )
  
  def to_secs_since_epoch_smear_utc(self, smear_plan: LeapSmearPlan) -> TimeStorageType:
    return self.time
  
  def to_date_tuple_smear_utc(self, smear_plan: LeapSmearPlan, date_cls: type[JulGregBaseDate] = GregorianDate) -> DateTupleBasic:
    return self.epoch_instant_to_date_tuple(self.to_secs_since_epoch_smear_utc(smear_plan), date_cls = date_cls)
  
  def get_date_object_smear_utc[T: JulGregBaseDate](self, smear_plan: LeapSmearPlan, date_cls: type[T] = GregorianDate) -> T:
    return date_cls(*self.to_date_tuple_smear_utc(smear_plan, date_cls = date_cls)[:3])
  
  def get_smear_utc_tai_offset(self, smear_plan: LeapSmearPlan) -> TimeStorageType:
    return self.to_secs_since_epoch_smear_utc(smear_plan) - self.time
  
  # > time zone
  
  @classmethod
  def from_secs_since_epoch_smear_tz(cls, smear_plan: LeapSmearPlan, time_zone: TimeZone, secs_since_epoch: TimeStorageType) -> Self:
    raise NotImplementedError()
  
  @classmethod
  def from_date_tuple_smear_tz(
    cls,
    smear_plan: LeapSmearPlan, time_zone: TimeZone,
    year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
    dst_second_fold: bool = False,
    round_invalid_dst_time_upwards: bool = True,
    date_cls: type[JulGregBaseDate] = GregorianDate
  ) -> Self:
    raise NotImplementedError()
  
  def to_secs_since_epoch_smear_tz(self, smear_plan: LeapSmearPlan, time_zone: TimeZone) -> TimeStorageType:
    raise NotImplementedError()
  
  def to_date_tuple_smear_tz(self, smear_plan: LeapSmearPlan, time_zone: TimeZone) -> DateTupleTZ:
    raise NotImplementedError()
  
  def get_date_object_smear_tz[T: JulGregBaseDate](self, smear_plan: LeapSmearPlan, time_zone: TimeZone, date_cls: type[T] = GregorianDate) -> T:
    raise NotImplementedError()
  
  def get_current_tz_offset_smear(self, smear_plan: LeapSmearPlan, time_zone: TimeZone, true_utc_offset: bool = False, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[FixedPrec, str | None]:
    raise NotImplementedError()
