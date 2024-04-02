import re
from math import floor, log10
from numbers import Integral
from typing import Self

class FixedPrec:
  __slots__ = 'value', 'place', 'max_prec'
  value: Integral
  place: Integral
  max_prec: Integral
  
  FLOAT_ADDED_PREC = 15
  _int_regex = re.compile('^(-?\\d+)$')
  _float_regex = re.compile('^(-?)(\\d+)\\.(\\d+)$')
  
  @classmethod
  def from_basic(cls, value: int | float | str | Self, max_prec: Integral = 12, cast_only: bool = False) -> Self:
    'Converts a value from a basic type like int, float, or FixedPrec to a FixedPrec.'
    if isinstance(value, int):
      return FixedPrec(value, 0, max_prec = max_prec)
    elif isinstance(value, float):
      # approximate conversion but floats are approximate anyway so
      prec = floor(log10(abs(value)))
      value /= 10 ** prec
      value *= 10 ** cls.FLOAT_ADDED_PREC
      return FixedPrec(int(value), -prec + cls.FLOAT_ADDED_PREC)
    elif isinstance(value, str) and not cast_only:
      if match := cls._int_regex.match(value):
        return FixedPrec(int(match[1]), 0, max_prec = max_prec)
      elif match := cls._float_regex.match(value):
        result = FixedPrec(int(match[2]) * 10 ** len(match[3]) + int(match[3]), len(match[3]), max_prec = max_prec)
        if match[1] == '-':
          result *= -1
        return result
      else:
        raise Exception(f'Could not convert string {value!r} to FixedPrec.')
    else:
      return value
  
  def __init__(self, *args: tuple[int | float | str] | tuple[Integral, Integral] | tuple[Integral, Integral, Integral], max_prec: Integral = 12):
    if len(args) == 0:
      raise Exception(f'FixedPrec constructor needs an argument')
    elif len(args) == 1:
      value = args[0]
      converted = self.from_basic(value, max_prec = max_prec)
      self.value = converted.value
      self.place = converted.place
      self.max_prec = converted.max_prec
    elif len(args) == 2:
      value, place = args
      self.value = value
      self.place = place
      self.max_prec = max_prec
    elif len(args) == 3:
      value, place, max_prec = args
      self.value = value
      self.place = place
      self.max_prec = max_prec
    else:
      raise Exception(f'FixedPrec constructor takes 1-3 arguments')
  
  def __repr__(self) -> str:
    return f'{self.__class__.__name__}(value = {self.value}, place = {self.place}, max_prec = {self.max_prec})'
  
  def __str__(self) -> str:
    if self.value == 0:
      if self.place <= 0:
        return '0'
      else:
        return f'0.{"0" * self.place}'
    else:
      if self.place <= 0:
        return f'{self.value}{"0" * (-self.place)}'
      else:
        negative = self.value < 0
        pos_string = str(abs(self.value))
        pos_string = f'{pos_string:0>{self.place + 1}}'
        return f'{"-" if negative else ""}{pos_string[:-self.place]}.{pos_string[-self.place:]}'
  
  def __format__(self, format_spec: str) -> str:
    if format_spec == '+':
      if self.value >= 0:
        return f'+{self!s}'
      else:
        return str(self)
    else:
      return NotImplemented
  
  def to_hashable_tuple(self) -> tuple[str, Integral, Integral, Integral]:
    return (self.__class__.__name__, self.value, self.place, self.max_prec)
  
  def __neg__(self) -> Self:
    return FixedPrec(
      -self.value,
      self.place,
      self.max_prec
    )
  
  def __int__(self):
    if self.place < 0:
      return int(self.value * 10 ** -self.place)
    elif self.place > 0:
      if self.value < 0:
        return int(-(-self.value // 10 ** self.place))
      else:
        return int(self.value // 10 ** self.place)
    else:
      return int(self.value)
  
  def __float__(self):
    if self.place < 0:
      return float(self.value) * 10.0 ** -self.place
    elif self.place > 0:
      return float(self.value) / 10.0 ** self.place
    else:
      return float(self.value)
  
  def reduce_to_max_prec(self) -> Self:
    if self.place > self.max_prec:
      return FixedPrec(
        self.value // 10 ** (self.place - self.max_prec),
        self.max_prec,
        self.max_prec
      )
    else:
      return self
  
  def convert_to_highest_precision(self, other: Self) -> Self:
    if self.place > other.place:
      precise = self
      less_precise = other
    else:
      precise = other
      less_precise = self
    
    place_diff = precise.place - less_precise.place
    
    less_precise_converted = FixedPrec(
      less_precise.value * (10 ** place_diff),
      precise.place,
      max(less_precise.max_prec, precise.max_prec)
    )
    
    if self.place > other.place:
      if self.max_prec < less_precise_converted.max_prec:
        self = FixedPrec(
          self.value,
          self.place,
          less_precise_converted.max_prec
        )
      
      return self, less_precise_converted
    else:
      if other.max_prec < less_precise_converted.max_prec:
        other = FixedPrec(
          other.value,
          other.place,
          less_precise_converted.max_prec
        )
      
      return less_precise_converted, other
  
  def __add__(self, other) -> Self:
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value + other.value,
      self.place,
      self.max_prec
    )
  
  def __sub__(self, other) -> Self:
    return self + (-other)
  
  def __mul__(self, other) -> Self:
    other = self.from_basic(other, cast_only = True)
    return FixedPrec(
      self.value * other.value,
      self.place + other.place,
      max(self.max_prec, other.max_prec)
    ).reduce_to_max_prec()
  
  def __floordiv__(self, other) -> Self:
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value // other.value,
      0,
      self.max_prec,
    )
  
  def __mod__(self, other) -> Self:
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value % other.value,
      self.place,
      self.max_prec
    )
  
  def __divmod__(self, other) -> Self:
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value // other.value,
      0,
      self.max_prec,
    ), FixedPrec(
      self.value % other.value,
      self.place,
      self.max_prec
    )
  
  def __radd__(self, other) -> Self:
    return self + other
  
  def __rsub__(self, other) -> Self:
    return (-self) + other
  
  def __rmul__(self, other) -> Self:
    return self * other
  
  def __eq__(self, other):
    if other is None:
      return False
    
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return self.value == other.value
  
  def __ne__(self, other):
    if other is None:
      return True
    
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return self.value != other.value
  
  def __gt__(self, other):
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return self.value > other.value
  
  def __lt__(self, other):
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return self.value < other.value
  
  def __ge__(self, other):
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return self.value >= other.value
  
  def __le__(self, other):
    other = self.from_basic(other, cast_only = True)
    self, other = self.convert_to_highest_precision(other)
    
    return self.value <= other.value
