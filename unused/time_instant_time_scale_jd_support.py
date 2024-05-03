class TimeInstant:
  # omitted beginning of file
  ...
  
  # @classmethod
  # def from_date_tuple_time_scale(cls, year: Integral, month: Integral, day: Integral, hour: Integral, minute: Integral, second: Integral, frac_second: TimeStorageType, second_fold: bool = False, round_invalid_time_upwards: bool = True, time_scale: TIME_SCALES = TIME_SCALES.TT, date_cls: type[DateBase] = GregorianDate) -> Self:
  #   '''
  #   Returns a timeinstant corresponding to the seconds since epoch tuple
  #   interpreted in the given time scale.
  #   Note: this function behaves differently than from_date_tuple_tai and
  #   from_date_tuple_utc, as those use the default timeinstant epoch, not
  #   a time scale specific epoch. Additionally, this function does not
  #   take seconds values over 59 in the UTC time scale.
  #   '''
  #   ...
  
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
