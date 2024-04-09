class TimeInstant:
  # omitted beginning of file
  ...
  
  # time scale support
  
  # https://en.wikipedia.org/wiki/Terrestrial_Time
  TT_OFFSET_FROM_TAI: FixedPrec = FixedPrec('32.184')
  
  TIME_SCALES = Enum('TIME_SCALES', [
    'TT',
    'TAI',
    'UTC',
  ])
  
  TIME_SCALE_INFO: dict[str, tuple[TimeStorageType, TimeStorageType]] = {
    # format:
    # <time_scale>: (time_rate, zero_time)
  }
  
  @classmethod
  def time_to_secs_since_epoch_time_scale(cls, time: TimeStorageType, time_scale: TIME_SCALES = TIME_SCALES.TT) -> TimeStorageType | tuple[TimeStorageType, bool]:
    ...
  
  @classmethod
  def secs_since_epoch_time_scale_to_time(cls, secs_since_epoch: TimeStorageType, second_fold: bool = False, time_scale: TIME_SCALES = TIME_SCALES.TT) -> TimeStorageType:
    ...
  
  @classmethod
  def from_secs_since_epoch_time_scale(cls, secs_since_epoch: TimeStorageType, second_fold: bool = False, time_scale: TIME_SCALES = TIME_SCALES.TT) -> Self:
    ...
  
  @classmethod
  def from_date_tuple_time_scale(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, second_fold: bool = False, round_invalid_time_upwards: bool = True, time_scale: TIME_SCALES = TIME_SCALES.TT, date_cls: type[DateBase] = GregorianDate) -> Self:
    '''
    Returns a timeinstant corresponding to the seconds since epoch tuple
    interpreted in the given time scale.
    Note: this function behaves differently than from_date_tuple_tai and
    from_date_tuple_utc, as those use the default timeinstant epoch, not
    a time scale specific epoch. Additionally, this function does not
    take seconds values over 59 in the UTC time scale.
    '''
    ...
  
  def to_secs_since_epoch_time_scale(self, time_scale: TIME_SCALES = TIME_SCALES.TT) -> TimeStorageType:
    return self.time_to_secs_since_epoch_time_scale(self._time, time_scale = time_scale)
  
  def to_date_tuple_time_scale(self, time_scale: TIME_SCALES = TIME_SCALES.TT) -> tuple[Integral, Integral, Integral, int, int, int, TimeStorageType] | tuple[Integral, Integral, Integral, int, int, int, TimeStorageType, bool]:
    ...
  
  # julian date support
  # https://en.wikipedia.org/wiki/Julian_day
  
  JULIAN_DATE_ORIGIN_TUPLE: tuple[int, int, int, int, int, int, int] = -4712, 1, 1, 12, 0, 0, 0
  REDUCED_JULIAN_DATE_OFFSET: FixedPrec = FixedPrec('-2400000')
  MODIFIED_JULIAN_DATE_OFFSET: FixedPrec = FixedPrec('-2400000.5')
  
  @classmethod
  def from_julian_date(cls, jd: TimeStorageType, second_fold: bool = False, time_scale: TIME_SCALES = TIME_SCALES.TT):
    origin_time = cls.time_to_secs_since_epoch_time_scale(
      cls.from_date_tuple_time_scale(*cls.JULIAN_DATE_ORIGIN_TUPLE, time_scale = time_scale, date_cls = JulianDate).time,
      time_scale = time_scale
    )
    
    if isinstance(origin_time, tuple):
      origin_time = origin_time[0]
    
    return cls.from_secs_since_epoch_time_scale(jd * cls.NOMINAL_SECS_PER_DAY + origin_time, second_fold = second_fold, time_scale = time_scale)
  
  @classmethod
  def from_reduced_julian_date(cls, jd: TimeStorageType, second_fold: bool = False, time_scale: TIME_SCALES = TIME_SCALES.TT):
    return cls.from_julian_date(jd - cls.REDUCED_JULIAN_DATE_OFFSET, second_fold = second_fold, time_scale = time_scale)
  
  @classmethod
  def from_modified_julian_date(cls, jd: TimeStorageType, second_fold: bool = False, time_scale: TIME_SCALES = TIME_SCALES.TT):
    return cls.from_julian_date(jd - cls.MODIFIED_JULIAN_DATE_OFFSET, second_fold = second_fold, time_scale = time_scale)
  
  def to_julian_date(self, time_scale: TIME_SCALES = TIME_SCALES.TT) -> TimeStorageType | tuple[TimeStorageType, bool]:
    self_time = self.to_secs_since_epoch_time_scale(time_scale = time_scale)
    origin_time = self.time_to_secs_since_epoch_time_scale(
      self.from_date_tuple_time_scale(*self.JULIAN_DATE_ORIGIN_TUPLE, time_scale = time_scale, date_cls = JulianDate).time,
      time_scale = time_scale
    )
    
    if isinstance(origin_time, tuple):
      origin_time = origin_time[0]
    
    if isinstance(self_time, tuple):
      return (self_time[0] - origin_time) / self.NOMINAL_SECS_PER_DAY, self_time[1]
    else:
      return (self_time - origin_time) / self.NOMINAL_SECS_PER_DAY
  
  def to_reduced_julian_date(self, time_scale: TIME_SCALES = TIME_SCALES.TT) -> TimeStorageType | tuple[TimeStorageType, bool]:
    jd = self.to_julian_date(time_scale = time_scale)
    
    if isinstance(jd, tuple):
      return jd[0] + self.REDUCED_JULIAN_DATE_OFFSET, jd[1]
    else:
      return jd[0] + self.REDUCED_JULIAN_DATE_OFFSET
  
  def to_modified_julian_date(self, time_scale: TIME_SCALES = TIME_SCALES.TT) -> TimeStorageType | tuple[TimeStorageType, bool]:
    jd = self.to_julian_date(time_scale = time_scale)
    
    if isinstance(jd, tuple):
      return jd[0] + self.MODIFIED_JULIAN_DATE_OFFSET, jd[1]
    else:
      return jd[0] + self.MODIFIED_JULIAN_DATE_OFFSET
