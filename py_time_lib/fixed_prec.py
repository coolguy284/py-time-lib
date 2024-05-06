import re
from math import floor, log10
from numbers import Integral, Real
from typing import Self

from .lib_funcs import binary_search_float

class FixedPrec(Real):
  # static stuff
  
  DEFAULT_MAX_PREC = 12
  FLOAT_ADDED_PREC = 15
  RADIX = 10
  RADIX_FLOAT = float(RADIX)
  ROUND_UP_THRESHOLD = RADIX // 2
  PI_STR = '3.14159265358979323846264338327950288419716939937510'
  PI_MAX_PREC = len(PI_STR) - 2
  # https://en.wikipedia.org/wiki/E_(mathematical_constant)
  E_STR = '2.7182818284590452353602874713526624977572'
  E_MAX_PREC = len(E_STR) - 2
  
  _int_regex = re.compile(r'^(-?\d+)$')
  _float_regex = re.compile(r'^(-?)(\d+)\.(\d+)$')
  
  # instance stuff
  __slots__ = 'value', 'place', 'max_prec'
  value: Integral
  place: Integral
  max_prec: Integral
  
  @classmethod
  def from_basic(cls, value: int | float | str | Self, max_prec: Integral = None, cast_only: bool = False) -> Self:
    'Converts a value from a basic type like int, float, or FixedPrec to a FixedPrec.'
    if isinstance(value, int):
      return cls(value, 0, max_prec = max_prec)
    elif isinstance(value, float):
      # approximate conversion but floats are approximate anyway so
      if value == 0:
        return cls(0, cls.FLOAT_ADDED_PREC)
      else:
        prec = floor(log10(abs(value)))
        scale_div = cls.RADIX ** prec
        if scale_div == 0:
          return cls(0, cls.FLOAT_ADDED_PREC)
        value /= cls.RADIX ** prec
        value *= cls.RADIX ** cls.FLOAT_ADDED_PREC
        return cls(int(value), -prec + cls.FLOAT_ADDED_PREC)
    elif isinstance(value, str):
      if not cast_only:
        if match := cls._int_regex.match(value):
          return cls(int(match[1]), 0, max_prec = max_prec)
        elif match := cls._float_regex.match(value):
          result = cls(int(match[2]) * cls.RADIX ** len(match[3]) + int(match[3]), len(match[3]), max_prec = max_prec)
          if match[1] == '-':
            result *= -1
          return result
        else:
          raise TypeError(f'Could not convert string {value!r} to {cls.__name__}.')
      else:
        raise TypeError(f'Cannot auto-cast string to {cls.__name__}')
    else:
      if hasattr(value, 'value') and hasattr(value, 'place') and hasattr(value, 'max_prec'):
        # duck typing
        if max_prec != None:
          return FixedPrec(value.value, value.place, max_prec = max_prec)
        else:
          return value
      else:
        raise TypeError(f'Could not convert object to {cls.__name__}')
  
  def __init__(self, *args: tuple[int | float | str] | tuple[Integral, Integral] | tuple[Integral, Integral, Integral], max_prec: Integral = None):
    if len(args) == 1:
      value = args[0]
      converted = self.from_basic(value, max_prec = max_prec)
      self.value = converted.value
      self.place = converted.place
      self.max_prec = converted.max_prec
    elif len(args) == 2:
      value, place = args
      self.value = value
      self.place = place
      self.max_prec = max_prec if max_prec != None else self.DEFAULT_MAX_PREC
    elif len(args) == 3:
      value, place, max_prec = args
      self.value = value
      self.place = place
      self.max_prec = max_prec if max_prec != None else self.DEFAULT_MAX_PREC
    else:
      raise TypeError(f'{self.__class__.__name__} constructor takes 1-3 arguments ({len(args)} given)')
  
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
  
  def to_data_tuple(self) -> tuple[str, Integral, Integral, Integral]:
    return (self.__class__.__name__, self.value, self.place, self.max_prec)
  
  def to_hashable_tuple(self) -> tuple[str, Integral, Integral]:
    return ('FixedPrec', self.value, self.place)
  
  def __hash__(self) -> int:
    if self.place <= 0:
      return hash(int(self))
    else:
      float_ver = float(self)
      if self == float_ver:
        return hash(float_ver)
      else:
        return hash(self.reduce_to_lowest_place().to_hashable_tuple())
  
  def __neg__(self) -> Self:
    return self.__class__(
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
      return int(self.value * self.RADIX ** -self.place)
    elif self.place > 0:
      if self.value < 0:
        return int(-(-self.value // self.RADIX ** self.place))
      else:
        return int(self.value // self.RADIX ** self.place)
    else:
      return int(self.value)
  
  def __float__(self):
    if self.place < 0:
      return float(self.value) * self.RADIX_FLOAT ** -self.place
    elif self.place > 0:
      return float(self.value) / self.RADIX_FLOAT ** self.place
    else:
      return float(self.value)
  
  def __complex__(self):
    return complex(float(self))
  
  def __floor__(self):
    if self.place <= 0:
      return self
    else:
      return self.__class__(self.value // self.RADIX ** self.place, max_prec = self.max_prec)
  
  def __ceil__(self):
    if self.place <= 0:
      return self
    else:
      return self.__class__(-(-self.value // self.RADIX ** self.place), max_prec = self.max_prec)
  
  def __trunc__(self):
    if self.place <= 0:
      return self
    else:
      if self.value < 0:
        return self.__class__(-(-self.value // self.RADIX ** self.place), max_prec = self.max_prec)
      else:
        return self.__class__(self.value // self.RADIX ** self.place, max_prec = self.max_prec)
  
  def __round__(self, ndigits: Integral = 0):
    if self.place <= ndigits:
      return self
    else:
      round_digit = (self.value // self.RADIX ** (self.place - ndigits - 1)) % self.RADIX
      
      if round_digit >= self.ROUND_UP_THRESHOLD:
        return self.__class__(-(-self.value // self.RADIX ** (self.place - ndigits)), ndigits, max_prec = self.max_prec)
      else:
        return self.__class__(self.value // self.RADIX ** (self.place - ndigits), ndigits, max_prec = self.max_prec)
  
  def reduce_to_max_prec(self) -> Self:
    if self.place > self.max_prec:
      return self.__class__(
        self.value // self.RADIX ** (self.place - self.max_prec),
        self.max_prec,
        self.max_prec
      )
    else:
      return self
  
  def increase_to_max_prec(self) -> Self:
    if self.place < self.max_prec:
      return self.__class__(
        self.value * self.RADIX ** (self.max_prec - self.place),
        self.max_prec,
        self.max_prec
      )
    else:
      return self
  
  def force_to_max_prec(self) -> Self:
    if self.place > self.max_prec:
      return self.__class__(
        self.value // self.RADIX ** (self.place - self.max_prec),
        self.max_prec,
        self.max_prec
      )
    elif self.place < self.max_prec:
      return self.__class__(
        self.value * self.RADIX ** (self.max_prec - self.place),
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
    
    less_precise_converted = self.__class__(
      less_precise.value * (self.RADIX ** place_diff),
      precise.place,
      max(less_precise.max_prec, precise.max_prec)
    )
    
    if self.place > other.place:
      if self.max_prec < less_precise_converted.max_prec:
        self = self.__class__(
          self.value,
          self.place,
          less_precise_converted.max_prec
        )
      
      return self, less_precise_converted
    else:
      if other.max_prec < less_precise_converted.max_prec:
        other = self.__class__(
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
      while value % self.RADIX == 0:
        value //= self.RADIX
        place -= 1
      result = self.__class__(value, place, self.max_prec)
    else:
      if result.place > 0:
        result = self.__class__(result.value, 0, self.max_prec)
    
    return result
  
  def __add__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.__class__(
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
    except TypeError:
      return NotImplemented
    
    return self.__class__(
      self.value * other.value,
      self.place + other.place,
      max(self.max_prec, other.max_prec)
    ).reduce_to_max_prec()
  
  def __floordiv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.__class__(
      self.value // other.value,
      0,
      self.max_prec
    )
  
  def __mod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.__class__(
      self.value % other.value,
      self.place,
      self.max_prec
    )
  
  def __divmod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    div, mod = divmod(self.value, other.value)
    
    return self.__class__(
      div,
      0,
      self.max_prec
    ), self.__class__(
      mod,
      self.place,
      self.max_prec
    )
  
  def __truediv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    if other.value == 0:
      raise ZeroDivisionError('division by zero')
    else:
      max_prec = max(self.max_prec, other.max_prec)
      additional_precision = max(len(str(other.value)) - len(str(self.value)) + max_prec, 0) + 1
      return self.__class__(
        self.value * self.RADIX ** additional_precision // other.value,
        self.place - other.place + additional_precision,
        max_prec
      ).reduce_to_max_prec()
  
  def _nthroot(self, other: Integral) -> Self:
    'Requires other be greater than or equal to 1, and self >= 0.'
    
    if other < 1:
      raise ValueError(f'Other must be greater than or equal to 1, got {other}')
    elif self < 0:
      raise ValueError(f'Cannot take root of negative number ({self.__class__.__name__} does not support complex numbers)')
    
    if other == 1:
      return self
    elif self == 1:
      return self
    else:
      if self < 1:
        return binary_search_float(lambda x: x ** other <= self, self.__class__(0, self.place, self.max_prec), 1)
      else:
        return binary_search_float(lambda x: x ** other <= self, 1, self)
  
  def __pow__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    if self == 1:
      return self
    
    other = other.reduce_to_lowest_place()
    
    if other < 0:
      if abs(self) > 2 and other < -200:
        return FixedPrec(0, 0, max_prec = max(self.max_prec, other.max_prec))
      else:
        return 1 / (self ** -other)
    elif other.place <= 0:
      # other is integral
      if other.value == 0:
        return self.__class__(1, 0, max(self.max_prec, other.max_prec))
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
      # other is fractional
      integral, fractional = divmod(other, 1)
      result = self ** integral
      self_root = self
      while fractional % 1 != 0:
        fractional *= self.RADIX
        fractional %= self.RADIX
        self_root = self_root._nthroot(self.RADIX)
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
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.__class__(
      other.value // self.value,
      0,
      self.max_prec
    )
  
  def __rmod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.__class__(
      other.value % self.value,
      self.place,
      self.max_prec
    )
  
  def __rdivmod__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    div, mod = divmod(other.value, self.value)
    
    return self.__class__(
      div,
      0,
      self.max_prec
    ), self.__class__(
      mod,
      self.place,
      self.max_prec
    )
  
  def __rtruediv__(self, other) -> Self:
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    if self.value == 0:
      raise ZeroDivisionError('division by zero')
    else:
      max_prec = max(other.max_prec, self.max_prec)
      additional_precision = max(len(str(self.value)) - len(str(other.value)) + max_prec, 0) + 1
      return self.__class__(
        other.value * self.RADIX ** additional_precision // self.value,
        other.place - self.place + additional_precision,
        max_prec
      ).reduce_to_max_prec()
  
  def __rpow__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    return other ** self
  
  def __eq__(self, other):
    if other is None:
      return False
    
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value == other.value
  
  def __ne__(self, other):
    if other is None:
      return True
    
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value != other.value
  
  def __gt__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value > other.value
  
  def __lt__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value < other.value
  
  def __ge__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
      return NotImplemented
    
    self, other = self.convert_to_highest_precision(other)
    
    return self.value >= other.value
  
  def __le__(self, other):
    try:
      other = self.from_basic(other, cast_only = True)
    except TypeError:
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
    return self.__class__(0)
  
  def smallest_representable(self):
    return FixedPrec(1, self.max_prec, max_prec = self.max_prec)
  
  def pi(self):
    if self.max_prec > self.PI_MAX_PREC:
      raise OverflowError(f'Cannot return pi to {self.max_prec} digits, max precision is {self.PI_MAX_PREC}')
    return FixedPrec(self.PI_STR, max_prec = self.max_prec).reduce_to_max_prec()
  
  def e(self):
    if self.max_prec > self.E_MAX_PREC:
      raise OverflowError(f'Cannot return pi to {self.max_prec} digits, max precision is {self.PI_MAX_PREC}')
    return FixedPrec(self.E_STR, max_prec = self.max_prec).reduce_to_max_prec()
  
  def exp(self) -> Self:
    return self.e() ** self
  
  def sin(self) -> Self:
    # x - x^3/3! + x^5/5! + ...
    PI = self.pi()
    PI1_2 = PI / 2
    if self < 0 or self > PI1_2:
      repeat, remainder = divmod(self, PI1_2)
      repeat %= 4
      if repeat % 2 == 0:
        initial = remainder.sin()
      else:
        initial = (PI1_2 - remainder).sin()
      if repeat >= 2:
        return -initial
      else:
        return initial
    else:
      self_sq = self * self
      x_prod = self
      total_sum = 0
      k = 0
      while x_prod > 0:
        total_sum += x_prod * (1 if k % 2 == 0 else -1)
        x_prod *= self_sq / ((2 * k + 2) * (2 * k + 3))
        k += 1
      return total_sum
  
  def cos(self) -> Self:
    PI = self.pi()
    PI1_2 = PI / 2
    return (self + PI1_2).sin()
  
  def tan(self) -> Self:
    return self.sin() / self.cos()
