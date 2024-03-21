class FixedPrec:
  __slots__ = 'value', 'place', 'max_prec'
  
  def __init__(self, value, place, max_prec = 12):
    self.value = value
    self.place = place
    self.max_prec = max_prec
  
  def __repr__(self):
    return f'FixedPrec(value = {self.value}, place = {self.place}, max_prec = {self.max_prec})'
  
  def __str__(self):
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
  
  def __neg__(self):
    return FixedPrec(
      -self.value,
      self.place,
      self.max_prec,
    )
  
  def convert_to_highest_precision(self, other):
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
  
  def __add__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return FixedPrec(
      self.value + other.value,
      self.place,
      self.max_prec
    )
  
  def __sub__(self, other):
    return self + (-other)
  
  def __eq__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return self.value == other.value
  
  def __ne__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return self.value != other.value
  
  def __gt__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return self.value > other.value
  
  def __lt__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return self.value < other.value
  
  def __ge__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return self.value >= other.value
  
  def __le__(self, other):
    self, other = self.convert_to_highest_precision(other)
    
    return self.value <= other.value
