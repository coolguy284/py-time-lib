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
  
  def __add__(self, other):
    if self.place > other.place:
      precise = self
      less_precise = other
    else:
      precise = other
      less_precise = self
    
    place_diff = precise.place - less_precise.place
    
    return FixedPrec(
      less_precise.value * (10 ** place_diff) + precise.value,
      precise.place,
      max(less_precise.max_prec, precise.max_prec)
    )
  
  def __sub__(self, other):
    return self + (-other)
