from enum import Enum
from numbers import Integral
from typing import Self

from ...fixed_prec import FixedPrec
from ...named_tuples import DateTupleBasic
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ..lib import TimeStorageType
from .time_inst_tz import TimeInstantTimeZones

class TimeInstMonotonic(TimeInstantTimeZones):
  # static stuff
  
  TIME_SCALES = Enum('TIME_SCALES', (
    'TAI',
    'TT',
    #'TCG',
    #'TCB',
    #'UT1',
    #'TIME_CENTER_GALAXY',
    #'TIME_COMOVING_FRAME',
  ))
  
  # https://en.wikipedia.org/wiki/Terrestrial_Time
  TT_OFFSET_FROM_TAI: FixedPrec = FixedPrec('32.184')
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_mono_secs_since_epoch(cls, time_scale: TIME_SCALES, mono_secs_since_epoch: TimeStorageType) -> Self:
    match time_scale:
      case cls.TIME_SCALES.TAI:
        return cls(mono_secs_since_epoch)
      
      case cls.TIME_SCALES.TT:
        return cls(mono_secs_since_epoch - cls.TT_OFFSET_FROM_TAI)
  
  @classmethod
  def from_date_tuple_mono(
    cls,
    time_scale: TIME_SCALES,
    year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
    date_cls: type[JulGregBaseDate] = GregorianDate
  ) -> Self:
    return cls.from_mono_secs_since_epoch(
      time_scale,
      cls.date_tuple_to_epoch_instant(year, month, day, hour, minute, second, frac_second, date_cls = date_cls)
    )
  
  def to_mono_secs_since_epoch(self, time_scale: TIME_SCALES) -> TimeStorageType:
    match time_scale:
      case self.TIME_SCALES.TAI:
        return self._time
      
      case self.TIME_SCALES.TT:
        return self._time + self.TT_OFFSET_FROM_TAI
  
  def to_date_tuple_mono(self, time_scale: TIME_SCALES, date_cls: type[JulGregBaseDate] = GregorianDate) -> DateTupleBasic:
    return self.epoch_instant_to_date_tuple(self.to_mono_secs_since_epoch(time_scale), date_cls = date_cls)
  
  def get_date_object_mono[T: JulGregBaseDate](self, time_scale: TIME_SCALES, date_cls: type[T] = GregorianDate) -> T:
    return date_cls(*self.to_date_tuple_mono(time_scale, date_cls = date_cls)[:3])
  
  def get_mono_tai_offset(self, time_scale: TIME_SCALES) -> TimeStorageType:
    return self.to_mono_secs_since_epoch(time_scale) - self.time
