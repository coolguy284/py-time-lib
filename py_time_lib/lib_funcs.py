from pathlib import PurePath
from numbers import Integral, Real
from os import makedirs
from os.path import exists
from typing import Callable, Sequence
from urllib.request import urlopen

MAX_BINARY_SEARCH_STEPS = 500
MAX_LINEAR_INVERSE_STEPS = 500

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
  past_low_enough = None
  past_too_high = None
  steps = 0
  
  while abs(too_high - low_enough) > epsilon and (low_enough != past_low_enough or too_high != past_too_high):
    past_low_enough = low_enough
    past_too_high = too_high
    
    guess = (low_enough + too_high) / 2
    if not func(guess):
      # too high
      too_high = guess
    else:
      # could be valid
      low_enough = guess
    
    steps += 1
    
    if steps > MAX_BINARY_SEARCH_STEPS:
      raise RuntimeError('Binary search float max steps reached')
  
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

def almost_linear_func_inverse[T: Real](func: Callable[[T], T], output: T, epsilon: Real = 0, min_val: T | None = None, max_val: T | None = None) -> T:
  guess = output
  
  if max_val != None:
    if guess > max_val:
      guess = max_val
  
  if min_val != None:
    if guess < min_val:
      guess = min_val
  
  steps = 0
  
  while abs((current_output := func(guess)) - output) > epsilon:
    delta = current_output - output
    
    guess -= delta
    
    if max_val != None:
      if guess > max_val:
        guess = max_val
    
    if min_val != None:
      if guess < min_val:
        guess = min_val
    
    steps += 1
    
    if steps > MAX_LINEAR_INVERSE_STEPS:
      raise RuntimeError('Linear inverse max steps reached')
  
  return guess

def almost_linear_func_inverse_deriv[T: Real](func: Callable[[T], T], output: T, epsilon: Real = 0, min_val: T | None = None, max_val: T | None = None, deriv_epsilon: Real = 1e-6) -> T:
  guess = output
  
  if max_val != None:
    if guess > max_val:
      guess = max_val
  
  if min_val != None:
    if guess < min_val:
      guess = min_val
  
  steps = 0
  
  while abs((current_output := func(guess)) - output) > epsilon:
    delta = current_output - output
    
    deriv_guess = guess + deriv_epsilon
    deriv_flip = False
    
    if max_val != None:
      if deriv_guess > max_val:
        deriv_guess = guess - deriv_epsilon
        deriv_flip = True
    
    deriv = (func(deriv_guess) - current_output) / deriv_epsilon
    if deriv_flip:
      deriv *= -1
    
    guess -= delta / deriv
    
    if max_val != None:
      if guess > max_val:
        guess = max_val
    
    if min_val != None:
      if guess < min_val:
        guess = min_val
    
    steps += 1
    
    if steps > MAX_LINEAR_INVERSE_STEPS:
      raise RuntimeError('Linear inverse max steps reached')
  
  return guess

def fancy_format(obj, indent = 2, _start_indent = 0) -> None:
  "An alternative to python's pprint that formats massive data in an easier to understand format, more akin to JSON indentation."
  base_indent = ' ' * _start_indent
  if isinstance(obj, list):
    if len(obj) == 0:
      return '[]'
    else:
      return \
        f'{base_indent}[\n' + \
          '\n'.join(f'{fancy_format(z, indent = indent, _start_indent = _start_indent + indent)},' for z in obj) + '\n' + \
        f'{base_indent}]'
  elif isinstance(obj, dict):
    if len(obj) == 0:
      return '{}'
    else:
      next_indent = base_indent + ' ' * indent
      return \
        f'{base_indent}{{\n' + \
          '\n'.join(
            (
              f'{next_indent}{z!r}: ' + \
              f'{fancy_format(obj[z], indent = indent, _start_indent = _start_indent + indent).strip()},'
            )
            for z in sorted(obj)
          ) + '\n' + \
        f'{base_indent}}}'
  else:
    return f'{base_indent}{obj!r}'

def file_relative_path_to_abs(file_path: str) -> str:
  # https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory/3430395#3430395
  return str(PurePath(__file__).parent / file_path)

def file_at_path_exists(file_path: str) -> bool:
  return exists(file_relative_path_to_abs(file_path))

def get_file_at_path(file_path: str) -> bytes | None:
  try:
    with open(file_relative_path_to_abs(file_path), 'rb') as f:
      return f.read()
  except FileNotFoundError:
    return None

def set_file_at_path(file_path: str, contents: bytes) -> None:
  abs_path = file_relative_path_to_abs(file_path)
  makedirs(PurePath(abs_path).parent, exist_ok = True)
  with open(abs_path, 'wb') as f:
    f.write(contents)

def get_file_from_online(url: str) -> bytes:
  response = urlopen(url)
  
  if response.status != 200:
    raise RuntimeError('Leap second request failed')
  
  return response.read()
