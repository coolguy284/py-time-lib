def binary_search(func, min_inclusive = 0, max_exclusive = 100):
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
