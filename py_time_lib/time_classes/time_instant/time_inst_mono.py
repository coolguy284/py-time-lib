from enum import Enum
from numbers import Integral
from typing import Self

from ...lib_funcs import binary_search_float
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
    'TCG',
    'TCB', # inaccurate
    'GALACTIC_COORDINATE_TIME', # complete estimates
    'UNIVERSE_COORDINATE_TIME', # complete estimates
    #'UT1',
  ))
  
  # https://en.wikipedia.org/wiki/Terrestrial_Time
  TT_OFFSET_FROM_TAI: FixedPrec = FixedPrec('32.184')
  TT_EPOCH_TAI_TUPLE: tuple = 1977, 1, 1, 0, 0, 0, 0
  TCG_TO_TT_LG: FixedPrec = FixedPrec(f'0.{'0' * 9}6969290134', max_prec = 19) # 0.6969290134e-10
  TCG_TO_TT_FACTOR: FixedPrec = 1 - TCG_TO_TT_LG # 0.9999999993030709866
  
  # from https://github.com/coolguy284/html5-time-standards
  # to get universe time, stuff will be done.
  #
  # thank you https://www.quora.com/How-much-faster-would-an-atomic-clock-in-intergalactic-space-run-compared-to-one-on-the-surface-of-the-Earth
  #
  # formula for time dialation: sqrt(1 - (v / c) ^ 2); v can be moving velocity, or it can be escape velocity in the case of gravitational time dialation, the formula works either case
  #
  # start with scaling factor of solar system's velocity in the milky way
  # https://en.wikipedia.org/wiki/Galactic_year
  # solar system speed rel to milky way: 230 km/s
  #
  # then add scaling factor of our current milky way position to intergalactic space
  # https://www.quora.com/How-much-faster-would-an-atomic-clock-in-intergalactic-space-run-compared-to-one-on-the-surface-of-the-Earth
  # escape velocity of milky way: 550 km/s
  #
  # then add scaling factor of milky way's speed relative to cmb
  # https://en.wikipedia.org/wiki/Milky_Way
  # milky way speed rel to cmb: 630 km/s
  
  SPEED_OF_LIGHT = FixedPrec(299_792_458, max_prec = 19)
  SUN_SPEED_IN_MILKY_WAY = FixedPrec(230_000, max_prec = 19)
  MILKY_WAY_ESCAPE_VEL = FixedPrec(550_000, max_prec = 19)
  MILKY_WAY_CMB_REL_SPEED = FixedPrec(630_000, max_prec = 19)
  
  @classmethod
  def _time_dilation_factor(cls, velocity: FixedPrec) -> FixedPrec:
    return (1 - (velocity / cls.SPEED_OF_LIGHT) ** 2)._nthroot(2)
  
  @classmethod
  def _init_class_vars(cls):
    super()._init_class_vars()
    cls.TT_EPOCH: TimeStorageType = cls.from_date_tuple_tai(*cls.TT_EPOCH_TAI_TUPLE).time
    cls.GALACTIC_COORDINATE_TIME_TO_TCB_FACTOR: FixedPrec = cls._time_dilation_factor(cls.SUN_SPEED_IN_MILKY_WAY) * cls._time_dilation_factor(cls.MILKY_WAY_ESCAPE_VEL)
    cls.UNIVERSE_COORDINATE_TIME_TO_TCB_FACTOR: FixedPrec = cls.GALACTIC_COORDINATE_TIME_TO_TCB_FACTOR * cls._time_dilation_factor(cls.MILKY_WAY_CMB_REL_SPEED)
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_mono_secs_since_epoch(cls, time_scale: TIME_SCALES, mono_secs_since_epoch: TimeStorageType) -> Self:
    'This function still uses the TimeInstant standard epoch of Jan 1, 1 BCE Proleptic Gregorian Calendar.'
    match time_scale:
      case cls.TIME_SCALES.TAI:
        return cls(mono_secs_since_epoch)
      
      case cls.TIME_SCALES.TT:
        return cls(mono_secs_since_epoch - cls.TT_OFFSET_FROM_TAI)
      
      case cls.TIME_SCALES.TCG:
        return cls((mono_secs_since_epoch - cls.TT_OFFSET_FROM_TAI - cls.TT_EPOCH) * cls.TCG_TO_TT_FACTOR + cls.TT_EPOCH)
      
      case _ if time_scale == cls.TIME_SCALES.TCB or time_scale == cls.TIME_SCALES.GALACTIC_COORDINATE_TIME or time_scale == cls.TIME_SCALES.UNIVERSE_COORDINATE_TIME:
        delta = abs(mono_secs_since_epoch - cls.TT_EPOCH) * FixedPrec('0.01')
        low = mono_secs_since_epoch - delta - cls.TT_OFFSET_FROM_TAI
        high = mono_secs_since_epoch + delta + cls.TT_OFFSET_FROM_TAI
        test = lambda x: cls(x).to_mono_secs_since_epoch(time_scale) <= mono_secs_since_epoch
        assert test(low)
        assert not test(high)
        return cls(binary_search_float(test, low, high))
  
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
    'This function still uses the TimeInstant standard epoch of Jan 1, 1 BCE Proleptic Gregorian Calendar.'
    match time_scale:
      case self.TIME_SCALES.TAI:
        return self._time
      
      case self.TIME_SCALES.TT:
        return self._time + self.TT_OFFSET_FROM_TAI
      
      case self.TIME_SCALES.TCG:
        return (self._time - self.TT_EPOCH) / self.TCG_TO_TT_FACTOR + self.TT_EPOCH + self.TT_OFFSET_FROM_TAI
      
      case self.TIME_SCALES.TCB:
        # https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems#TDT_-_TDB,_TCB
        J2000_EPOCH = self.from_date_tuple_mono(self.TIME_SCALES.TT, 2000, 1, 1, 0, 0, 0, 0).time
        
        T = (self._time - J2000_EPOCH) / (36525 * 86400)
        g = (FixedPrec('3.141592653589') / 180) * (FixedPrec('357.528') + FixedPrec('35999.050') * T)
        TDB = self._time + self.TT_OFFSET_FROM_TAI + FixedPrec('0.001658') * (g + FixedPrec('0.0167') * g.sin()).sin()
        LB = FixedPrec(f'0.{'0' * 7}155051976772', max_prec = 19) # 1.55051976772e-8
        P0 = FixedPrec(f'0.{'0' * 4}65510') # 6.5510e-5
        TCB = TDB + LB * (self._time - self.TT_EPOCH) + P0
        return TCB
      
      case self.TIME_SCALES.GALACTIC_COORDINATE_TIME:
        TCB = self.to_mono_secs_since_epoch(self.TIME_SCALES.TCB)
        GALACTIC_COORDINATE_TIME = (TCB - self.TT_EPOCH) / self.GALACTIC_COORDINATE_TIME_TO_TCB_FACTOR + self.TT_EPOCH
        return GALACTIC_COORDINATE_TIME
      
      case self.TIME_SCALES.UNIVERSE_COORDINATE_TIME:
        TCB = self.to_mono_secs_since_epoch(self.TIME_SCALES.TCB)
        UNIVERSE_COORDINATE_TIME = (TCB - self.TT_EPOCH) / self.UNIVERSE_COORDINATE_TIME_TO_TCB_FACTOR + self.TT_EPOCH
        return UNIVERSE_COORDINATE_TIME
  
  def to_date_tuple_mono(self, time_scale: TIME_SCALES, date_cls: type[JulGregBaseDate] = GregorianDate) -> DateTupleBasic:
    return self.epoch_instant_to_date_tuple(self.to_mono_secs_since_epoch(time_scale), date_cls = date_cls)
  
  def get_date_object_mono[T: JulGregBaseDate](self, time_scale: TIME_SCALES, date_cls: type[T] = GregorianDate) -> T:
    return date_cls(*self.to_date_tuple_mono(time_scale, date_cls = date_cls)[:3])
  
  def get_mono_tai_offset(self, time_scale: TIME_SCALES) -> TimeStorageType:
    return self.to_mono_secs_since_epoch(time_scale) - self.time