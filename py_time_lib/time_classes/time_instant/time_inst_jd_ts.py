from typing import Self

from ...fixed_prec import FixedPrec
from ...calendars.julian import JulianDate
from ..lib import TimeStorageType
from .time_inst_tz import TimeInstantTimeZones

class TimeInstantJulianDateAndUnixTimestamp(TimeInstantTimeZones):
  # static stuff
  
  # https://en.wikipedia.org/wiki/Julian_day
  JULIAN_DATE_ORIGIN_TUPLE: tuple[int, int, int, int, int, int, int] = -4712, 1, 1, 12, 0, 0, 0
  REDUCED_JULIAN_DATE_OFFSET_FROM_JD: FixedPrec = FixedPrec('-2400000')
  MODIFIED_JULIAN_DATE_OFFSET_FROM_JD: FixedPrec = FixedPrec('-2400000.5')
  
  @classmethod
  def _init_class_vars(cls) -> None:
    # https://stackoverflow.com/questions/1817183/using-super-with-a-class-method/47247072#47247072
    super()._init_class_vars()
    
    # basic functionality of TimeInstant created by this point so TimeInstant methods can be called
    
    cls.UNIX_TIMESTAMP_ORIGIN_OFFSET: TimeStorageType = cls.from_date_tuple_utc(1970, 1, 1, 0, 0, 0, 0).to_utc_secs_since_epoch()[0]
    cls.JULIAN_DATE_OFFSET: TimeStorageType = cls.from_date_tuple_tai(*cls.JULIAN_DATE_ORIGIN_TUPLE, date_cls = JulianDate).time
  
  # instance stuff
  
  __slots__ = ()
  
  @classmethod
  def from_unix_timestamp(cls, unix_secs_since_epoch: TimeStorageType, second_fold: bool = False) -> Self:
    return cls.from_utc_secs_since_epoch(unix_secs_since_epoch + cls.UNIX_TIMESTAMP_ORIGIN_OFFSET, second_fold)
  
  @classmethod
  def from_julian_date_tai(cls, julian_date: TimeStorageType) -> Self:
    return cls((julian_date * cls.NOMINAL_SECS_PER_DAY) + cls.JULIAN_DATE_OFFSET)
  
  @classmethod
  def from_reduced_julian_date_tai(cls, reduced_julian_date: TimeStorageType) -> Self:
    return cls.from_julian_date_tai(reduced_julian_date - cls.REDUCED_JULIAN_DATE_OFFSET_FROM_JD)
  
  @classmethod
  def from_modified_julian_date_tai(cls, modified_julian_date: TimeStorageType) -> Self:
    return cls.from_julian_date_tai(modified_julian_date - cls.MODIFIED_JULIAN_DATE_OFFSET_FROM_JD)
  
  def to_unix_timestamp(self) -> tuple[TimeStorageType, bool]:
    '''
    Returns a unix timestamp tuple in the form of (unix_secs_since_epoch, second_fold).
    After a positive leap second, the counter gets set back one second and second_fold
    becomes true for one second.
    '''
    utc_secs_since_epoch, second_fold = self.to_utc_secs_since_epoch()
    unix_secs_since_epoch = utc_secs_since_epoch - self.UNIX_TIMESTAMP_ORIGIN_OFFSET
    return unix_secs_since_epoch, second_fold
  
  def to_julian_date_tai(self) -> TimeStorageType:
    return (self.time - self.JULIAN_DATE_OFFSET) / self.NOMINAL_SECS_PER_DAY
  
  def to_reduced_julian_date_tai(self) -> TimeStorageType:
    return self.to_julian_date_tai() + self.REDUCED_JULIAN_DATE_OFFSET_FROM_JD
  
  def to_modified_julian_date_tai(self) -> TimeStorageType:
    return self.to_julian_date_tai() + self.MODIFIED_JULIAN_DATE_OFFSET_FROM_JD
