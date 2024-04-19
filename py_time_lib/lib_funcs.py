from numbers import Integral, Real
from typing import Callable, Sequence

def binary_search[T: Integral](func: Callable[[T], bool], min_inclusive: T = 0, max_exclusive: T = 100) -> T:
  'Finds the largest integer value x so that func(x) is True, in interval [min, max), using a binary search.'
  
  low_enough = min_inclusive
  too_high = max_exclusive
  while too_high - low_enough > 1:
    guess = (low_enough + too_high) // 2
    if not func(guess):
      # too high
      too_high = guess
    else:
      # could be valid
      low_enough = guess
  
  return low_enough

def binary_search_float[T: Real](func: Callable[[T], bool], min_inclusive: T = 0.0, max_exclusive: T = 100.0, epsilon: T = 0.0) -> T:
  'Finds the largest real value x so that func(x) is True, in interval [min, max), using a binary search.'
  
  low_enough = min_inclusive
  too_high = max_exclusive
  past_low_enough = low_enough
  past_too_high = too_high
  
  while too_high - low_enough > epsilon and (low_enough != past_low_enough or too_high != past_too_high):
    past_low_enough = low_enough
    past_too_high = too_high
    
    guess = (low_enough + too_high) / 2
    if not func(guess):
      # too high
      too_high = guess
    else:
      # could be valid
      low_enough = guess
  
  return low_enough

def binary_search_array_split[T](array: Sequence[T], func: Callable[[T], bool]) -> tuple[Sequence[T], Sequence[T]]:
  'Splits array into section where func(array[i]) is True (must be lower part) and where it is False.'
  
  if len(array) == 0:
    return [], []
  elif len(array) == 1:
    if func(array[0]):
      return array, []
    else:
      return [], array
  else:
    if not func(array[0]):
      return [], array
    
    largest_true_index = binary_search(lambda x: func(array[x]), 0, len(array))
    
    return array[:largest_true_index + 1], array[largest_true_index + 1:]
