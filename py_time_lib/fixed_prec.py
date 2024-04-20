import re
from math import floor, log10
from numbers import Complex, Integral
from typing import Self

from .lib_funcs import binary_search_float

class FixedPrec(Complex):
  __slots__ = 'value', 'place', 'max_prec'
  value: Integral
  place: Integral
  max_prec: Integral
  
  FLOAT_ADDED_PREC = 15
  _int_regex = re.compile(r'^(-?\d+)$')
  _float_regex = re.compile(r'^(-?)(\d+)\.(\d+)$')
  
  @classmethod
  def from_basic(cls, value: int | float | str | Self, max_prec: Integral = 12, cast_only: bool = False) -> Self:
    'Converts a value from a basic type like int, float, or FixedPrec to a FixedPrec.'
    if isinstance(value, int):
      return cls(value, 0, max_prec = max_prec)
    elif isinstance(value, float):
      # approximate conversion but floats are approximate anyway so
      if value == 0:
        return cls(0, cls.FLOAT_ADDED_PREC)
      else:
        prec = floor(log10(abs(value)))
        value /= 10 ** prec
        value *= 10 ** cls.FLOAT_ADDED_PREC
        return cls(int(value), -prec + cls.FLOAT_ADDED_PREC)
    elif isinstance(value, str) and not cast_only:
      if match := cls._int_regex.match(value):
        return cls(int(match[1]), 0, max_prec = max_prec)
      elif match := cls._float_regex.match(value):
        result = cls(int(match[2]) * 10 ** len(match[3]) + int(match[3]), len(match[3]), max_prec = max_prec)
        if match[1] == '-':
          result *= -1
        return result
      else:
        raise Exception(f'Could not convert string {value!r} to {cls.__name__}.')
    else:
      if hasattr(value, 'value') and hasattr(value, 'place') and hasattr(value, 'max_prec'):
        # duck typing
        return value
      else:
        raise NotImplementedError()
  
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
    if self.place > 0:
      return f'{self.__class__.__name__}({str(self)!r})'
    else:
      return f'{self.__class__.__name__}({self!s})'
  
  def __str__(self) -> str:
    if self.value == 0:
      if self.place <= 0:
        return '0'
      else:
        return f'0.{'0' * self.place}'
    else:
      if self.place <= 0:
        return f'{self.value}{'0' * (-self.place)}'
      else:
        negative = self.value < 0
        pos_string = str(abs(self.value))
        pos_string = f'{pos_string:0>{self.place + 1}}'
        return f'{'-' if negative else ''}{pos_string[:-self.place]}.{pos_string[-self.place:]}'
  
  def __format__(self, format_spec: str) -> str:
    if format_spec == '':
      return str(self)
    elif format_spec == '+':
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
  
  def __pos__(self) -> Self:
    return self
  
  def __abs__(self) -> Self:
    if self < 0:
      return -self
    else:
      return self
  
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
  
  def __complex__(self):
    return complex(float(self))
  
  def reduce_to_max_prec(self) -> Self:
    if self.place > self.max_prec:
      return FixedPrec(
        self.value // 10 ** (self.place - self.max_prec),
        self.max_prec,
        self.max_prec
      )
    else:
      return self
  
  def increase_to_max_prec(self) -> Self:
    if self.place < self.max_prec:
      return FixedPrec(
        self.value * 10 ** (self.max_prec - self.place),
        self.max_prec,
        self.max_prec
      )
    else:
      return self
  
  def force_to_max_prec(self) -> Self:
    if self.place > self.max_prec:
      return FixedPrec(
        self.value // 10 ** (self.place - self.max_prec),
        self.max_prec,
        self.max_prec
      )
    elif self.place < self.max_prec:
      return FixedPrec(
        self.value * 10 ** (self.max_prec - self.place),
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
  
  def reduce_to_lowest_place(self) -> Self:
    result = self
    
    if result.value != 0:
      value = result.value
      place = result.place
      while value % 10 == 0:
        value //= 10
        place -= 1
      result = self.__class__(value, place, self.max_prec)
    else:
      if result.place > 0:
        result = self.__class__(result.value, 0, self.max_prec)
    
    return result
  
  def __add__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value + other.value,
      self.place,
      self.max_prec
    )
  
  def __sub__(self, other) -> Self:
    try:
      return self + (-other)
    except TypeError:
      return NotImplemented
  
  def __mul__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    return FixedPrec(
      self.value * other.value,
      self.place + other.place,
      max(self.max_prec, other.max_prec)
    ).reduce_to_max_prec()
  
  def __floordiv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value // other.value,
      0,
      self.max_prec,
    )
  
  def __mod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value % other.value,
      self.place,
      self.max_prec
    )
  
  def __divmod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    div, mod = divmod(self.value, other.value)
    
    return FixedPrec(
      div,
      0,
      self.max_prec,
    ), FixedPrec(
      mod,
      self.place,
      self.max_prec
    )
  
  def __truediv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    if other.value == 0:
      raise ZeroDivisionError('division by zero')
    else:
      max_prec = max(self.max_prec, other.max_prec)
      additional_precision = max(len(str(other.value)) - len(str(self.value)) + max_prec, 0) + 1
      return FixedPrec(
        self.value * 10 ** additional_precision // other.value,
        self.place - other.place + additional_precision,
        max_prec
      ).reduce_to_max_prec()
  
  def _nthroot(self, other: Integral) -> Self:
    'Requires other be greater than or equal to 1, and self >= 0.'
    
    if other < 1:
      raise Exception(f'Other must be greater than or equal to 1, got {other}')
    elif self < 0:
      raise Exception(f'Cannot take root of negative number ({self.__class__.__name__} does not support complex numbers)')
    
    if other == 1:
      return self
    elif self == 1:
      return self
    else:
      if self < 1:
        return binary_search_float(lambda x: x ** other <= self, FixedPrec(0, self.place, self.max_prec), 1)
      else:
        return binary_search_float(lambda x: x ** other <= self, 1, self)
  
  def __pow__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    if self == 1:
      return self
    elif self < 0:
      raise Exception(f'{self.__class__.__name__} cannot handle complex output (negative base)')
    
    other = other.reduce_to_lowest_place()
    
    if other < 0:
      return 1 / (self ** -other)
    elif other.place <= 0:
      # other is integral
      if other.value == 0:
        return FixedPrec(1, 0, max(self.max_prec, other.max_prec))
      elif other.value == 1 and other.place == 0:
        return self
      else:
        result = 1
        factor = self
        remaining_exp = int(other)
        while remaining_exp > 0:
          remaining_exp, current = divmod(remaining_exp, 2)
          if current > 0:
            result *= factor
          factor *= factor
        return result
    else:
      integral, fractional = divmod(other, 1)
      result = self ** integral
      self_root = self
      while fractional % 1 != 0:
        fractional *= 10
        self_root = self_root._nthroot(10)
        frac_power = int(fractional // 1)
        result *= self_root ** frac_power
      return result
  
  def __radd__(self, other) -> Self:
    try:
      return self + other
    except TypeError:
      return NotImplemented
  
  def __rsub__(self, other) -> Self:
    try:
      return (-self) + other
    except TypeError:
      return NotImplemented
  
  def __rmul__(self, other) -> Self:
    try:
      return self * other
    except TypeError:
      return NotImplemented
  
  def __rfloordiv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      other.value // self.value,
      0,
      self.max_prec,
    )
  
  def __rmod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      other.value % self.value,
      self.place,
      self.max_prec,
    )
  
  def __rdivmod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    div, mod = divmod(other.value, self.value)
    
    return FixedPrec(
      div,
      0,
      self.max_prec,
    ), FixedPrec(
      mod,
      self.place,
      self.max_prec
    )
  
  def __rtruediv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    if self.value == 0:
      raise ZeroDivisionError('division by zero')
    else:
      max_prec = max(other.max_prec, self.max_prec)
      additional_precision = max(len(str(self.value)) - len(str(other.value)) + max_prec, 0) + 1
      return FixedPrec(
        other.value * 10 ** additional_precision // self.value,
        other.place - self.place + additional_precision,
        max_prec
      ).reduce_to_max_prec()
  
  def __rpow__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    if other == 1:
      return other
    elif other < 0:
      raise Exception(f'{other.__class__.__name__} cannot handle complex output (negative base)')
    
    self = self.reduce_to_lowest_place()
    
    if self < 0:
      return 1 / (other ** -self)
    elif self.place <= 0:
      # self is integral
      if self.value == 0:
        return FixedPrec(1, 0, max(other.max_prec, self.max_prec))
      elif self.value == 1 and self.place == 0:
        return other
      else:
        result = 1
        factor = other
        remaining_exp = int(self)
        while remaining_exp > 0:
          remaining_exp, current = divmod(remaining_exp, 2)
          if current > 0:
            result *= factor
          factor *= factor
        return result
    else:
      integral, fractional = divmod(self, 1)
      result = other ** integral
      self_root = other
      while fractional % 1 != 0:
        fractional *= 10
        self_root = self_root._nthroot(10)
        frac_power = int(fractional // 1)
        result *= self_root ** frac_power
      return result
  
  def __eq__(self, other):
    if other is None:
      return False
    
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value == other.value
  
  def __ne__(self, other):
    if other is None:
      return True
    
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value != other.value
  
  def __gt__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value > other.value
  
  def __lt__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value < other.value
  
  def __ge__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value >= other.value
  
  def __le__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except NotImplementedError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value <= other.value
  
  def conjugate(self) -> Self:
    return self
  
  @property
  def real(self) -> Self:
    return self
  
  @property
  def imag(self) -> Self:
    return FixedPrec(0)
