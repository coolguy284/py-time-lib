from numbers import Integral
from typing import Self

from ...lib_funcs import almost_linear_func_inverse_deriv
from ...calendars.jul_greg_base import JulGregBaseDate
from ...calendars.gregorian import GregorianDate
from ...fixed_prec import FixedPrec
from ..lib import TimeStorageType
from .time_inst_mono import TimeInstMonotonic
from ...named_tuples import DateTupleBasic

class TimeInstantSolar(TimeInstMonotonic):
  # static stuff
  
  DEGREES_PER_HOUR_ROTATION = 15
  # https://en.wikipedia.org/wiki/Tropical_year
  UT1_SECS_PER_TROPICAL_YEAR = FixedPrec('365.24217') * TimeInstMonotonic.NOMINAL_SECS_PER_DAY
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_secs_since_epoch_solar(cls, longitude_deg: TimeStorageType, true_solar_time: bool, secs_since_epoch_solar: TimeStorageType) -> Self:
    if true_solar_time:
      secs_since_epoch_solar = FixedPrec.from_basic(secs_since_epoch_solar)
      # https://en.wikipedia.org/wiki/Equation_of_time
      return cls.from_secs_since_epoch_solar(
        longitude_deg,
        False,
        almost_linear_func_inverse_deriv(
          lambda x: cls.from_secs_since_epoch_solar(longitude_deg, False, x).to_secs_since_epoch_solar(longitude_deg, True),
          secs_since_epoch_solar,
          epsilon = secs_since_epoch_solar.smallest_representable() * 2
        )
      )
    else:
      return cls.from_secs_since_epoch_mono(
        cls.TIME_SCALES.UT1,
        secs_since_epoch_solar - longitude_deg * (cls.NOMINAL_SECS_PER_HOUR // cls.DEGREES_PER_HOUR_ROTATION)
      )
  
  @classmethod
  def from_date_tuple_solar(
    cls,
    longitude_deg: TimeStorageType, true_solar_time: bool,
    year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType,
    date_cls: type[JulGregBaseDate] = GregorianDate
  ) -> Self:
    return cls.from_secs_since_epoch_solar(
      longitude_deg,
      true_solar_time,
      cls.date_tuple_to_epoch_instant(year, month, day, hour, minute, second, frac_second, date_cls = date_cls)
    )
  
  def to_secs_since_epoch_solar(self, longitude_deg: TimeStorageType, true_solar_time: bool) -> TimeStorageType:
    if true_solar_time:
      ut1_secs_since_epoch = self.to_secs_since_epoch_mono(self.TIME_SCALES.UT1)
      secs_since_year_start = ut1_secs_since_epoch % self.UT1_SECS_PER_TROPICAL_YEAR
      # https://en.wikipedia.org/wiki/Equation_of_time
      D: FixedPrec = FixedPrec('6.24004077') + secs_since_year_start * 2 * ut1_secs_since_epoch.pi() / self.UT1_SECS_PER_TROPICAL_YEAR
      true_mean_delta = (FixedPrec('-7.659') * D.sin() + FixedPrec('9.863') * (2 * D + FixedPrec('3.5932')).sin()) * 60
      return self.to_secs_since_epoch_solar(longitude_deg, False) + true_mean_delta
    else:
      ut1_secs_since_epoch = self.to_secs_since_epoch_mono(self.TIME_SCALES.UT1)
      return ut1_secs_since_epoch + longitude_deg * (self.NOMINAL_SECS_PER_HOUR // self.DEGREES_PER_HOUR_ROTATION)
  
  def to_date_tuple_solar(self, longitude_deg: TimeStorageType, true_solar_time: bool, date_cls: type[JulGregBaseDate] = GregorianDate) -> DateTupleBasic:
    return self.epoch_instant_to_date_tuple(self.to_secs_since_epoch_solar(longitude_deg, true_solar_time), date_cls = date_cls)
  
  def get_date_object_solar[T: JulGregBaseDate](self, longitude_deg: TimeStorageType, true_solar_time: bool, date_cls: type[T] = GregorianDate) -> T:
    return date_cls(*self.to_date_tuple_solar(longitude_deg, true_solar_time, date_cls = date_cls)[:3])
  
  def get_solar_tai_offset(self, longitude_deg: TimeStorageType, true_solar_time: bool) -> TimeStorageType:
    return self.to_secs_since_epoch_solar(longitude_deg, true_solar_time) - self.time
