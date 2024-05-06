from dataclasses import dataclass, field
from enum import Enum
from numbers import Integral
from typing import NamedTuple, Self
from weakref import WeakValueDictionary

from ...lib_funcs import binary_search, almost_linear_func_inverse_deriv
from ...calendars.date_delta import DateDelta
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
  'BUMP',
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
  'SMEAR',
))

@dataclass
class TAIToUTCSmearEntry:
  mode: SmearTableEntryMode
  tai_secs_since_epoch: TimeStorageType
  smear_secs_since_epoch: TimeStorageType
  # format:
  # {
  #   if mode == 'FIXED_OFFSET':
  #     'smear_tai_offset': FixedPrec seconds,
  #   elif mode == 'SMEAR':
  #     'smear_type': SmearType,
  #     'smear_length': FixedPrec seconds,
  #     'leap_extra_secs': FixedPrec seconds,
  # }
  data: dict[str, FixedPrec]

@dataclass
class UTCSmearToTAIEntry:
  mode: SmearTableEntryMode
  tai_secs_since_epoch: TimeStorageType
  smear_secs_since_epoch: TimeStorageType
  # format:
  # {
  #   if mode == 'FIXED_OFFSET':
  #     'tai_smear_offset': FixedPrec seconds,
  #   elif mode == 'SMEAR':
  #     'smear_type': SmearType,
  #     'smear_length': FixedPrec seconds,
  #     'leap_extra_secs': FixedPrec seconds,
  # }
  data: dict[str, FixedPrec]

@dataclass
class LeapSmearPlan():
  # static stuff
  
  @staticmethod
  def date_to_tai_start(date: GregorianDate) -> FixedPrec:
    'Returns the start time of the leap second that occured at the end of date.'
    day_after_leap = date + DateDelta(1)
    window_end_tai = TimeInstant.from_date_tuple_utc(*day_after_leap.to_date_tuple(), 0, 0, 0, 0).time
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
    self.utc_smear_tai_initial_offset = TimeInstant.UTC_INITIAL_OFFSET_FROM_TAI
    self.tai_to_utc_smear_table = []
    self.utc_smear_to_tai_table = []
    
    for i in range(len(TimeInstant.TAI_TO_UTC_OFFSET_TABLE)):
      leap_entry = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[i]
      
      if leap_entry['leap_utc_delta'] <= 0:
        # positive leap second
        if leap_entry['positive_leap_second_occurring']:
          add_entry = True
        else:
          add_entry = False
      else:
        # negative leap second
        add_entry = True
      
      if add_entry:
        if leap_entry['start_instant'] in self.smear_overrides:
          smear_profile = self.smear_overrides[leap_entry['start_instant']]
        else:
          smear_profile = self.default_smear
        
        if smear_profile.start_basis == LeapBasis.START:
          smear_start_tai = leap_entry['start_instant'] - smear_profile.secs_before_start_basis
        else:
          smear_start_tai = leap_entry['start_instant'] - leap_entry['leap_utc_delta'] - smear_profile.secs_before_start_basis
        
        if smear_profile.end_basis == LeapBasis.START:
          smear_end_tai = leap_entry['start_instant'] + smear_profile.secs_after_end_basis
        else:
          smear_end_tai = leap_entry['start_instant'] - leap_entry['leap_utc_delta'] + smear_profile.secs_after_end_basis
        
        if not leap_entry['positive_leap_second_occurring']:
          # for negative leap second, leap_entry['start_instant'] is more like end instant
          smear_start_tai += leap_entry['leap_utc_delta']
          smear_end_tai += leap_entry['leap_utc_delta']
        
        tai_length = smear_end_tai - smear_start_tai
        smear_length = tai_length + leap_entry['leap_utc_delta']
        
        if leap_entry['positive_leap_second_occurring']:
          start_utc_tai_offset = leap_entry['utc_epoch_secs'] - leap_entry['start_instant']
          end_utc_tai_offset = start_utc_tai_offset + leap_entry['leap_utc_delta']
        else:
          end_utc_tai_offset = leap_entry['utc_tai_delta']
          start_utc_tai_offset = end_utc_tai_offset - leap_entry['leap_utc_delta']
        
        smear_start_utc = smear_start_tai + start_utc_tai_offset
        smear_end_utc = smear_end_tai + end_utc_tai_offset
        
        self.tai_to_utc_smear_table.append(TAIToUTCSmearEntry(SmearTableEntryMode.SMEAR, smear_start_tai, smear_start_utc, {
          'smear_type': smear_profile.type,
          'smear_length': smear_length,
          'leap_extra_secs': -leap_entry['leap_utc_delta'],
        }))
        
        self.tai_to_utc_smear_table.append(TAIToUTCSmearEntry(SmearTableEntryMode.FIXED_OFFSET, smear_end_tai, smear_end_utc, {
          'smear_tai_offset': end_utc_tai_offset,
        }))
        
        self.utc_smear_to_tai_table.append(UTCSmearToTAIEntry(SmearTableEntryMode.SMEAR, smear_start_tai, smear_start_utc, {
          'smear_type': smear_profile.type,
          'smear_length': smear_length,
          'leap_extra_secs': -leap_entry['leap_utc_delta'],
        }))
        
        self.utc_smear_to_tai_table.append(UTCSmearToTAIEntry(SmearTableEntryMode.FIXED_OFFSET, smear_end_tai, smear_end_utc, {
          'tai_smear_offset': -end_utc_tai_offset,
        }))
  
  def __post_init__(self):
    self._generate_tables()
    _active_smear_plans[id(self)] = self

_active_smear_plans: WeakValueDictionary[int, LeapSmearPlan] = WeakValueDictionary()

class TimeInstantLeapSmear(TimeInstMonotonic):
  # static stuff
  
  @staticmethod
  def _bump_pos(num: FixedPrec) -> FixedPrec:
    'Function is 0 when num <= 0, and rises smoothly when num > 0.'
    if num <= 0:
      return FixedPrec(0)
    else:
      return (-1 / num).exp()
  
  @staticmethod
  def _bump_0_to_1(num: FixedPrec) -> FixedPrec:
    'Function is 0 when num <= 0, 1 when num >= 1, and rises smoothly in the middle.'
    return TimeInstantLeapSmear._bump_pos(num) / (TimeInstantLeapSmear._bump_pos(num) + TimeInstantLeapSmear._bump_pos(1 - num))
  
  @staticmethod
  def to_smear(smear_type: SmearType, smear_length: TimeStorageType, leap_extra_secs: TimeStorageType, tai_time_in_smear: TimeStorageType) -> FixedPrec:
    tai_time_in_smear = FixedPrec.from_basic(tai_time_in_smear)
    tai_length = smear_length + leap_extra_secs
    
    if not (0 <= tai_time_in_smear <= tai_length):
      raise ValueError(f'Tai time out of range: 0 <= tai_time <= {tai_length}; tai_time is {tai_time_in_smear}')
    
    if tai_time_in_smear == 0:
      return tai_time_in_smear
    elif tai_time_in_smear == tai_length:
      return tai_time_in_smear - leap_extra_secs
    else:
      match smear_type:
        case SmearType.LINEAR:
          return tai_time_in_smear * smear_length / tai_length
        
        case _ if smear_type == SmearType.COSINE or smear_type == SmearType.BUMP:
          tai_time_in_smear = FixedPrec.from_basic(tai_time_in_smear)
          epsilon = tai_time_in_smear.smallest_representable() * 2
          if smear_length * 0.1 < tai_time_in_smear < smear_length * 0.9:
            # low precision on middle
            epsilon *= 500_000
          return almost_linear_func_inverse_deriv(
            lambda x: TimeInstantLeapSmear.from_smear(smear_type, smear_length, leap_extra_secs, x),
            tai_time_in_smear,
            epsilon = epsilon,
            min_val = 0,
            max_val = smear_length,
            deriv_epsilon = tai_time_in_smear.smallest_representable() * 10
          )
  
  @staticmethod
  def from_smear(smear_type: SmearType, smear_length: TimeStorageType, leap_extra_secs: TimeStorageType, smear_time_in_smear: TimeStorageType) -> FixedPrec:
    smear_time_in_smear = FixedPrec.from_basic(smear_time_in_smear)
    
    if not (0 <= smear_time_in_smear <= smear_length):
      raise ValueError(f'Tai time out of range: 0 <= smear_time <= {smear_length}; smear_time is {smear_time_in_smear}')
    
    if smear_time_in_smear == 0:
      return smear_time_in_smear
    elif smear_time_in_smear == smear_length:
      return smear_time_in_smear + leap_extra_secs
    else:
      match smear_type:
        case SmearType.LINEAR:
          tai_length = smear_length + leap_extra_secs
          return smear_time_in_smear * tai_length / smear_length
        
        case SmearType.COSINE:
          # https://googleblog.blogspot.com/2011/09/time-technology-and-leaping-seconds.html
          half_leap_time = leap_extra_secs / 2
          return half_leap_time - half_leap_time * (smear_time_in_smear.pi() * smear_time_in_smear / smear_length).cos() + smear_time_in_smear
        
        case SmearType.BUMP:
          return leap_extra_secs * TimeInstantLeapSmear._bump_0_to_1(smear_time_in_smear / smear_length) + smear_time_in_smear
  
  # instance stuff
  
  __slots__ = ()
  
  # > utc
  
  @classmethod
  def from_secs_since_epoch_smear_utc(cls, smear_plan: LeapSmearPlan, secs_since_epoch: TimeStorageType) -> Self:
    if len(smear_plan.utc_smear_to_tai_table) == 0:
      return cls(secs_since_epoch - smear_plan.utc_smear_tai_initial_offset)
    else:
      if secs_since_epoch < smear_plan.utc_smear_to_tai_table[0].smear_secs_since_epoch:
        return cls(secs_since_epoch - smear_plan.utc_smear_tai_initial_offset)
      else:
        table_index = binary_search(lambda x: smear_plan.utc_smear_to_tai_table[x].smear_secs_since_epoch <= secs_since_epoch, 0, len(smear_plan.utc_smear_to_tai_table))
        smear_entry = smear_plan.utc_smear_to_tai_table[table_index]
        if smear_entry.mode == SmearTableEntryMode.FIXED_OFFSET:
          return cls(secs_since_epoch + smear_entry.data['tai_smear_offset'])
        else:
          return cls(cls.from_smear(smear_entry.data['smear_type'], smear_entry.data['smear_length'], smear_entry.data['leap_extra_secs'], secs_since_epoch - smear_entry.smear_secs_since_epoch) + smear_entry.tai_secs_since_epoch)
  
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
    if len(smear_plan.tai_to_utc_smear_table) == 0:
      return self.time + smear_plan.utc_smear_tai_initial_offset
    else:
      if self.time < smear_plan.tai_to_utc_smear_table[0].tai_secs_since_epoch:
        return self.time + smear_plan.utc_smear_tai_initial_offset
      else:
        table_index = binary_search(lambda x: smear_plan.tai_to_utc_smear_table[x].tai_secs_since_epoch <= self.time, 0, len(smear_plan.tai_to_utc_smear_table))
        smear_entry = smear_plan.tai_to_utc_smear_table[table_index]
        if smear_entry.mode == SmearTableEntryMode.FIXED_OFFSET:
          return self.time + smear_entry.data['smear_tai_offset']
        else:
          return self.to_smear(smear_entry.data['smear_type'], smear_entry.data['smear_length'], smear_entry.data['leap_extra_secs'], self.time - smear_entry.tai_secs_since_epoch) + smear_entry.smear_secs_since_epoch
  
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
