from math import log10
from py_time_lib import FixedPrec

from constants import time_min_exp, time_max_exp, time_linear_frac
from constants import time_rate_center_radius, time_rate_min_exp, time_rate_max_exp, time_rate_linear_frac

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

def time_rate_true_to_norm(time_rate: FixedPrec) -> float:
  if time_rate == 0:
    return 0.5
  else:
    forwards = time_rate > 0
    mul = 1 if forwards else -1
    rate_abs = abs(time_rate)
    norm_abs = exponential_to_linear(time_rate_linear_frac, time_rate_min_exp, time_rate_max_exp, rate_abs)
    return 0.5 + mul * (norm_abs * (0.5 - time_rate_center_radius) + time_rate_center_radius)

def time_rate_norm_to_true(time_rate_norm: float) -> tuple[FixedPrec, float]:
  if 0.5 - time_rate_center_radius / 2 < time_rate_norm < 0.5 + time_rate_center_radius / 2:
    return FixedPrec(0), 0.5
  else:
    forwards = time_rate_norm > 0.5
    mul = 1 if forwards else -1
    norm_abs = max(
      (abs(time_rate_norm - 0.5) - time_rate_center_radius) / (0.5 - time_rate_center_radius),
      0
    )
    return (
      mul * linear_to_exponential(time_rate_linear_frac, time_rate_min_exp, time_rate_max_exp, norm_abs),
      0.5 + mul * (norm_abs * (0.5 - time_rate_center_radius) + time_rate_center_radius),
    )

def time_norm_to_true_delta(time_norm: float) -> FixedPrec:
  norm_abs = abs(time_norm - 0.5) * 2
  positive = time_norm >= 0.5
  mul = 1 if positive else -1
  return mul * linear_to_exponential(time_linear_frac, time_min_exp, time_max_exp, norm_abs)

def time_delta_to_time_norm(time_delta: FixedPrec) -> float:
  delta_abs = abs(time_delta)
  mul = 1 if time_delta >= 0 else -1
  norm_abs = exponential_to_linear(time_linear_frac, time_min_exp, time_max_exp, delta_abs)
  return (mul * norm_abs) * 0.5 + 0.5
