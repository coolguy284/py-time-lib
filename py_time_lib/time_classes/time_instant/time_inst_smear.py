from dataclasses import dataclass
from enum import Enum
from numbers import Integral
from typing import NamedTuple, Self

from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
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

class TimeInstantLeapSmear(TimeInstMonotonic):
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
