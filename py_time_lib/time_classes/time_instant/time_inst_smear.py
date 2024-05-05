from dataclasses import dataclass, field
from enum import Enum
from numbers import Integral
from typing import NamedTuple, Self

from ...lib_funcs import binary_search_float
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ...fixed_prec import FixedPrec
from ..lib import TimeStorageType
from ...named_tuples import DateTupleBasic, DateTupleTZ
from .time_inst_mono import TimeInstMonotonic
from ..time_zone import TimeZone

LeapBasis = Enum('LeapBasis', (
  'START',
  'END',
))

SmearType = Enum('SmearType', (
  'LINEAR',
  'COSINE',
))

@dataclass(frozen = True)
class LeapSmearSingle():
  start_basis: LeapBasis
  secs_before_start_basis: TimeStorageType
  end_basis: LeapBasis
  secs_after_end_basis: TimeStorageType
  type: SmearType

class LeapSmearOverrideEntry(NamedTuple):
  leap_start_tai_secs_since_epoch: TimeStorageType
  smear: LeapSmearSingle

@dataclass(frozen = True)
class LeapSmearPlan():
  default_smear: LeapSmearSingle
  smear_overrides: tuple[LeapSmearOverrideEntry, ...]
  #e: int = field(init = False)
  
  def __post_init__(self):
    ...#object.__setattr__(self, 'e', 't')

class TimeInstantLeapSmear(TimeInstMonotonic):
  # static stuff
  
  @staticmethod
  def to_linear_smear(length: TimeStorageType, leap_extra_time: TimeStorageType, tai_time_in_smear: TimeStorageType) -> TimeStorageType:
    tai_length = length + leap_extra_time
    
    if not (0 <= tai_time_in_smear <= tai_length):
      raise ValueError(f'Tai time out of range: 0 <= tai_time <= {tai_length}; tai_time is {tai_time_in_smear}')
    
    return tai_time_in_smear * length / tai_length
  
  @staticmethod
  def from_linear_smear(length: TimeStorageType, leap_extra_time: TimeStorageType, smear_time_in_smear: TimeStorageType) -> TimeStorageType:
    if not (0 <= smear_time_in_smear <= length):
      raise ValueError(f'Tai time out of range: 0 <= smear_time <= {length}; smear_time is {smear_time_in_smear}')
    
    tai_length = length + leap_extra_time
    
    return smear_time_in_smear * tai_length / length
  
  @staticmethod
  def to_cosine_smear(length: TimeStorageType, leap_extra_time: TimeStorageType, tai_time_in_smear: TimeStorageType) -> FixedPrec:
    tai_time_in_smear = FixedPrec.from_basic(tai_time_in_smear)
    tai_length = length + leap_extra_time
    
    if not (0 <= tai_time_in_smear <= tai_length):
      raise ValueError(f'Tai time out of range: 0 <= tai_time <= {tai_length}; tai_time is {tai_time_in_smear}')
    
    if tai_time_in_smear == 0:
      return tai_time_in_smear
    elif tai_time_in_smear == tai_length:
      return tai_time_in_smear - leap_extra_time
    else:
      return binary_search_float(lambda x: TimeInstantLeapSmear.from_cosine_smear(length, leap_extra_time, x) <= tai_time_in_smear, 0, FixedPrec.from_basic(length))
  
  @staticmethod
  def from_cosine_smear(length: TimeStorageType, leap_extra_time: TimeStorageType, smear_time_in_smear: TimeStorageType) -> FixedPrec:
    if not (0 <= smear_time_in_smear <= length):
      raise ValueError(f'Tai time out of range: 0 <= smear_time <= {length}; smear_time is {smear_time_in_smear}')
    
    smear_time_in_smear = FixedPrec.from_basic(smear_time_in_smear)
    # https://googleblog.blogspot.com/2011/09/time-technology-and-leaping-seconds.html
    half_leap_time = leap_extra_time / 2
    
    if smear_time_in_smear == 0:
      return smear_time_in_smear
    elif smear_time_in_smear == length:
      return smear_time_in_smear + leap_extra_time
    else:
      return half_leap_time - half_leap_time * (smear_time_in_smear.pi() * smear_time_in_smear / length).cos() + smear_time_in_smear
  
  # instance stuff
  
  __slots__ = ()
  
  # > utc
  
  @classmethod
  def from_secs_since_epoch_smear_utc(self, smear_plan: LeapSmearPlan, secs_since_epoch: TimeStorageType) -> Self:
    ...
  
  @classmethod
  def from_date_tuple_smear_utc(
    self,
    smear_plan: LeapSmearPlan,
    year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
    date_cls: type[JulGregBaseDate] = GregorianDate
  ) -> Self:
    ...
  
  def to_secs_since_epoch_smear_utc(self, smear_plan: LeapSmearPlan) -> TimeStorageType:
    ...
  
  def to_date_tuple_smear_utc(self, smear_plan: LeapSmearPlan) -> DateTupleBasic:
    ...
  
  def get_date_object_smear_utc[T: JulGregBaseDate](self, smear_plan: LeapSmearPlan, date_cls: type[T] = GregorianDate) -> T:
    ...
  
  def get_smear_utc_tai_offset(self, smear_plan: LeapSmearPlan) -> TimeStorageType:
    ...
  
  # > time zone
  
  @classmethod
  def from_secs_since_epoch_smear_tz(self, smear_plan: LeapSmearPlan, time_zone: TimeZone, secs_since_epoch: TimeStorageType) -> Self:
    ...
  
  @classmethod
  def from_date_tuple_smear_utc(
    self,
    smear_plan: LeapSmearPlan, time_zone: TimeZone,
    year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
    dst_second_fold: bool = False,
    round_invalid_dst_time_upwards: bool = True,
    date_cls: type[JulGregBaseDate] = GregorianDate
  ) -> Self:
    ...
  
  def to_secs_since_epoch_smear_tz(self, smear_plan: LeapSmearPlan, time_zone: TimeZone) -> TimeStorageType:
    ...
  
  def to_date_tuple_smear_tz(self, smear_plan: LeapSmearPlan, time_zone: TimeZone) -> DateTupleTZ:
    ...
  
  def get_date_object_smear_tz[T: JulGregBaseDate](self, smear_plan: LeapSmearPlan, time_zone: TimeZone, date_cls: type[T] = GregorianDate) -> T:
    ...
  
  def get_current_tz_offset_smear(self, smear_plan: LeapSmearPlan, time_zone: TimeZone, true_utc_offset: bool = False, date_cls: type[JulGregBaseDate] = GregorianDate) -> tuple[FixedPrec, str | None]:
    ...
