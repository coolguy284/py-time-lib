from enum import Enum
from math import log10
from py_time_lib import FixedPrec

def linear_to_exponential(linear_start_frac: float, min_exp: float, max_exp: float, value: float) -> FixedPrec:
  if value <= linear_start_frac:
    return FixedPrec(10) ** min_exp * value / linear_start_frac
  else:
    return FixedPrec(10) ** (
      min_exp +
      (value - linear_start_frac) /
      (1 - linear_start_frac) *
      (max_exp - min_exp)
    )

def exponential_to_linear(linear_start_frac: float, min_exp: float, max_exp: float, value: FixedPrec) -> float:
  lin_threshold = FixedPrec(10) ** min_exp
  if value <= lin_threshold:
    return float(value / lin_threshold) * linear_start_frac
  else:
    return linear_start_frac + \
      (log10(value) - min_exp) / (max_exp - min_exp) * (1 - linear_start_frac)

TimeMode = Enum('TimeMode', (
  'CURRENT',
  'LEAP_SEC_REPLAY',
  'CUSTOMIZABLE',
))

RunMode = Enum('RunMode', (
  'CLOCK',
  'TIME_STANDARDS',
  'CALENDARS',
  'BLANK',
))
run_mode_names = {
  RunMode.CLOCK: 'Clock',
  RunMode.TIME_STANDARDS: 'Time Standards',
  RunMode.CALENDARS: 'Calendars (UTC)',
  RunMode.BLANK: 'Blank',
}
run_modes = list(RunMode)

LineStyles = Enum('LineStyles', (
  'THIN',
  'THICK',
  'ORANGE',
  'GREEN',
))
