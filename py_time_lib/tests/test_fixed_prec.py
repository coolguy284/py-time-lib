import unittest

from .. import FixedPrec

class TestFixedPrec(unittest.TestCase):
  def test_str(self):
    self.assertEqual(str(FixedPrec(0, -3)), '0')
    self.assertEqual(str(FixedPrec(0, 0)), '0')
    self.assertEqual(str(FixedPrec(0, 3)), '0.000')
    self.assertEqual(str(FixedPrec(1, -3)), '1000')
    self.assertEqual(str(FixedPrec(1, 0)), '1')
    self.assertEqual(str(FixedPrec(1, 3)), '0.001')
    self.assertEqual(str(FixedPrec(1003, 3)), '1.003')
    self.assertEqual(str(FixedPrec(1000, 3)), '1.000')
    self.assertEqual(str(FixedPrec(-1, -3)), '-1000')
    self.assertEqual(str(FixedPrec(-1, 0)), '-1')
    self.assertEqual(str(FixedPrec(-1, 3)), '-0.001')
    self.assertEqual(str(FixedPrec(-1003, 3)), '-1.003')
    self.assertEqual(str(FixedPrec(-1000, 3)), '-1.000')
  
  def test_format(self):
    self.assertEqual(f'{FixedPrec(1, 0):+}', '+1')
    self.assertEqual(f'{FixedPrec(0, 0):+}', '+0')
    self.assertEqual(f'{FixedPrec(-1, 0):+}', '-1')
    self.assertEqual(f'{FixedPrec(1, 0)}', '1')
    self.assertEqual(f'{FixedPrec(0, 0)}', '0')
    self.assertEqual(f'{FixedPrec(-1, 0)}', '-1')
  
  def test_neg(self):
    self.assertEqual(str(-FixedPrec(1, 0)), '-1')
    self.assertEqual(str(-FixedPrec(0, 0)), '0')
    self.assertEqual(str(-FixedPrec(-1, 0)), '1')
  
  def test_pos(self):
    self.assertEqual(+FixedPrec(3), 3)
    self.assertEqual(+FixedPrec(0), 0)
    self.assertEqual(+FixedPrec(-3), -3)
  
  def test_abs(self):
    self.assertEqual(abs(FixedPrec(3)), 3)
    self.assertEqual(abs(FixedPrec(0)), 0)
    self.assertEqual(abs(FixedPrec(-3)), 3)
  
  def test_add(self):
    self.assertEqual(str(FixedPrec(1, 0) + FixedPrec(3, 0)), '4')
    self.assertEqual(str(FixedPrec(1, 0) + FixedPrec(3, 3)), '1.003')
    self.assertEqual(str(FixedPrec(1, 0) + FixedPrec(3, -3)), '3001')
    self.assertEqual(str(FixedPrec(1, 0) - FixedPrec(3, 0)), '-2')
    self.assertEqual(str(FixedPrec(1, 0) - FixedPrec(3, 3)), '0.997')
    self.assertEqual(str(FixedPrec(1, 0) - FixedPrec(3, -3)), '-2999')
    
    self.assertEqual((FixedPrec(3) + 5).to_hashable_tuple(), ('FixedPrec', 8, 0, 12))
    self.assertEqual((5 + FixedPrec(3)).to_hashable_tuple(), ('FixedPrec', 8, 0, 12))
  
  def test_mul(self):
    self.assertEqual(str(FixedPrec(1, 0) * FixedPrec(3, 0)), '3')
    self.assertEqual(str(FixedPrec(8, 0) * FixedPrec(12, 0)), '96')
    self.assertEqual(str(FixedPrec(8, 0) * FixedPrec(12, 1)), '9.6')
    self.assertEqual(str(FixedPrec(8, 1) * FixedPrec(12, 1)), '0.96')
    self.assertEqual(str(FixedPrec(8, 1) * FixedPrec(12, 20)), '0.000000000000')
    
    self.assertEqual((FixedPrec(3) * 5).to_hashable_tuple(), ('FixedPrec', 15, 0, 12))
    self.assertEqual((5 * FixedPrec(3)).to_hashable_tuple(), ('FixedPrec', 15, 0, 12))
  
  def test_div_mod(self):
    self.assertEqual(FixedPrec('-21.0') // FixedPrec('10.0'), -3)
    self.assertEqual(FixedPrec('-11.0') // FixedPrec('10.0'), -2)
    self.assertEqual(FixedPrec('-10.0') // FixedPrec('10.0'), -1)
    self.assertEqual(FixedPrec('-9.0') // FixedPrec('10.0'), -1)
    self.assertEqual(FixedPrec('-1.0') // FixedPrec('10.0'), -1)
    self.assertEqual(FixedPrec('0.0') // FixedPrec('10.0'), 0)
    self.assertEqual(FixedPrec('9.0') // FixedPrec('10.0'), 0)
    self.assertEqual(FixedPrec('10.0') // FixedPrec('10.0'), 1)
    self.assertEqual(FixedPrec('12.0') // FixedPrec('10.0'), 1)
    self.assertEqual(FixedPrec('20.0') // FixedPrec('10.0'), 2)
    self.assertEqual(FixedPrec('22.0') // FixedPrec('10.0'), 2)
    
    self.assertEqual(FixedPrec('-21.0') % FixedPrec('10.0'), FixedPrec('9.0'))
    self.assertEqual(FixedPrec('-11.0') % FixedPrec('10.0'), FixedPrec('9.0'))
    self.assertEqual(FixedPrec('-10.0') % FixedPrec('10.0'), FixedPrec('0.0'))
    self.assertEqual(FixedPrec('-9.0') % FixedPrec('10.0'), FixedPrec('1.0'))
    self.assertEqual(FixedPrec('-1.0') % FixedPrec('10.0'), FixedPrec('9.0'))
    self.assertEqual(FixedPrec('0.0') % FixedPrec('10.0'), FixedPrec('0.0'))
    self.assertEqual(FixedPrec('9.0') % FixedPrec('10.0'), FixedPrec('9.0'))
    self.assertEqual(FixedPrec('10.0') % FixedPrec('10.0'), FixedPrec('0.0'))
    self.assertEqual(FixedPrec('12.0') % FixedPrec('10.0'), FixedPrec('2.0'))
    self.assertEqual(FixedPrec('20.0') % FixedPrec('10.0'), FixedPrec('0.0'))
    self.assertEqual(FixedPrec('22.0') % FixedPrec('10.0'), FixedPrec('2.0'))
    
    self.assertEqual(divmod(FixedPrec('-21.0'), FixedPrec('10.0')), (-3, FixedPrec('9.0')))
    self.assertEqual(divmod(FixedPrec('-11.0'), FixedPrec('10.0')), (-2, FixedPrec('9.0')))
    self.assertEqual(divmod(FixedPrec('-10.0'), FixedPrec('10.0')), (-1, FixedPrec('0.0')))
    self.assertEqual(divmod(FixedPrec('-9.0'), FixedPrec('10.0')), (-1, FixedPrec('1.0')))
    self.assertEqual(divmod(FixedPrec('-1.0'), FixedPrec('10.0')), (-1, FixedPrec('9.0')))
    self.assertEqual(divmod(FixedPrec('0.0'), FixedPrec('10.0')), (0, FixedPrec('0.0')))
    self.assertEqual(divmod(FixedPrec('9.0'), FixedPrec('10.0')), (0, FixedPrec('9.0')))
    self.assertEqual(divmod(FixedPrec('10.0'), FixedPrec('10.0')), (1, FixedPrec('0.0')))
    self.assertEqual(divmod(FixedPrec('12.0'), FixedPrec('10.0')), (1, FixedPrec('2.0')))
    self.assertEqual(divmod(FixedPrec('20.0'), FixedPrec('10.0')), (2, FixedPrec('0.0')))
    self.assertEqual(divmod(FixedPrec('22.0'), FixedPrec('10.0')), (2, FixedPrec('2.0')))
    
    self.assertEqual((FixedPrec(11) // 3).to_hashable_tuple(), ('FixedPrec', 3, 0, 12))
    self.assertEqual((11 // FixedPrec(3)).to_hashable_tuple(), ('FixedPrec', 3, 0, 12))
    
    self.assertEqual((FixedPrec(11) % 3).to_hashable_tuple(), ('FixedPrec', 2, 0, 12))
    self.assertEqual((11 % FixedPrec(3)).to_hashable_tuple(), ('FixedPrec', 2, 0, 12))
    
    self.assertEqual(tuple(x.to_hashable_tuple() for x in divmod(FixedPrec(11), 3)), (('FixedPrec', 3, 0, 12), ('FixedPrec', 2, 0, 12)))
    self.assertEqual(tuple(x.to_hashable_tuple() for x in divmod(11, FixedPrec(3))), (('FixedPrec', 3, 0, 12), ('FixedPrec', 2, 0, 12)))
  
  def test_true_div(self):
    self.assertEqual(FixedPrec(1) / FixedPrec(2), FixedPrec('0.5'))
    self.assertEqual(FixedPrec(9) / FixedPrec(3), FixedPrec(3))
    self.assertEqual(FixedPrec(9, -1) / FixedPrec(3), FixedPrec(30))
    self.assertEqual(FixedPrec(9, 1) / FixedPrec(3), FixedPrec('0.3'))
    self.assertEqual(FixedPrec(9) / FixedPrec(3, -1), FixedPrec('0.3'))
    self.assertEqual(FixedPrec(9) / FixedPrec(3, 1), FixedPrec(30))
    self.assertEqual(FixedPrec(1) / FixedPrec('0.25'), FixedPrec(4))
    self.assertEqual(FixedPrec(1) / FixedPrec('0.250000000000'), FixedPrec(4))
    self.assertEqual(FixedPrec(1) / FixedPrec('0.2500000000000'), FixedPrec(4))
    
    self.assertEqual((FixedPrec(12) / 3).to_hashable_tuple(), ('FixedPrec', 4_000_000_000_000, 12, 12))
    self.assertEqual((12 / FixedPrec(3)).to_hashable_tuple(), ('FixedPrec', 4_000_000_000_000, 12, 12))
  
  def test_relational(self):
    self.assertEqual(FixedPrec(1, 0) == FixedPrec(1, 0), True)
    self.assertEqual(FixedPrec(1, 0) == FixedPrec(10, 1), True)
    self.assertEqual(FixedPrec(1, 0) == FixedPrec(10, 0), False)
    self.assertEqual(FixedPrec(1, 0) != FixedPrec(1, 0), False)
    self.assertEqual(FixedPrec(1, 0) != FixedPrec(10, 1), False)
    self.assertEqual(FixedPrec(1, 0) != FixedPrec(10, 0), True)
    self.assertEqual(FixedPrec(1, 0) > FixedPrec(-1, 0), True)
    self.assertEqual(FixedPrec(1, 0) < FixedPrec(10, 0), True)
    self.assertEqual(FixedPrec(1, 0) >= FixedPrec(-1, 0), True)
    self.assertEqual(FixedPrec(1, 0) <= FixedPrec(10, 0), True)
    self.assertEqual(FixedPrec(1, 0) == None, False)
    self.assertEqual(FixedPrec(1, 0) != None, True)
    
    self.assertEqual(1 == FixedPrec(1, 0), True)
    self.assertEqual(1 == FixedPrec(10, 1), True)
    self.assertEqual(1 == FixedPrec(10, 0), False)
    self.assertEqual(1 != FixedPrec(1, 0), False)
    self.assertEqual(1 != FixedPrec(10, 1), False)
    self.assertEqual(1 != FixedPrec(10, 0), True)
    self.assertEqual(1 > FixedPrec(-1, 0), True)
    self.assertEqual(1 < FixedPrec(10, 0), True)
    self.assertEqual(1 >= FixedPrec(-1, 0), True)
    self.assertEqual(1 <= FixedPrec(10, 0), True)
    
    self.assertEqual(FixedPrec(1, 0) == 1, True)
    self.assertEqual(FixedPrec(1, 0) == 1, True)
    self.assertEqual(FixedPrec(1, 0) == 10, False)
    self.assertEqual(FixedPrec(1, 0) != 1, False)
    self.assertEqual(FixedPrec(1, 0) != 1, False)
    self.assertEqual(FixedPrec(1, 0) != 10, True)
    self.assertEqual(FixedPrec(1, 0) > -1, True)
    self.assertEqual(FixedPrec(1, 0) < 10, True)
    self.assertEqual(FixedPrec(1, 0) >= -1, True)
    self.assertEqual(FixedPrec(1, 0) <= 10, True)
  
  def test_to_int(self):
    self.assertEqual(int(FixedPrec('0')), 0)
    self.assertEqual(int(FixedPrec('0.0')), 0)
    self.assertEqual(int(FixedPrec(0, -1)), 0)
    self.assertEqual(int(FixedPrec('0.9')), 0)
    self.assertEqual(int(FixedPrec('-0.9')), 0)
    self.assertEqual(int(FixedPrec('3.9')), 3)
    self.assertEqual(int(FixedPrec('-3.9')), -3)
    self.assertEqual(int(FixedPrec(39, -1)), 390)
    self.assertEqual(int(FixedPrec(-39, -1)), -390)
    self.assertEqual(int(FixedPrec('4')), 4)
    self.assertEqual(int(FixedPrec('-4')), -4)
  
  def test_to_float(self):
    self.assertEqual(float(FixedPrec('0')), 0.0)
    self.assertEqual(float(FixedPrec('0.0')), 0.0)
    self.assertEqual(float(FixedPrec(0, -1)), 0.0)
    self.assertEqual(float(FixedPrec('0.9')), 0.9)
    self.assertEqual(float(FixedPrec('-0.9')), -0.9)
    self.assertEqual(float(FixedPrec('3.9')), 3.9)
    self.assertEqual(float(FixedPrec('-3.9')), -3.9)
    self.assertEqual(float(FixedPrec(39, -1)), 390.0)
    self.assertEqual(float(FixedPrec(-39, -1)), -390.0)
    self.assertEqual(float(FixedPrec('4')), 4.0)
    self.assertEqual(float(FixedPrec('-4')), -4.0)
  
  def test_to_hashable_tuple(self):
    self.assertEqual(FixedPrec(0, -3).to_hashable_tuple(), ('FixedPrec', 0, -3, 12))
    self.assertEqual(FixedPrec(0, 0).to_hashable_tuple(), ('FixedPrec', 0, 0, 12))
    self.assertEqual(FixedPrec(0, 3).to_hashable_tuple(), ('FixedPrec', 0, 3, 12))
    self.assertEqual(FixedPrec(1, -3).to_hashable_tuple(), ('FixedPrec', 1, -3, 12))
    self.assertEqual(FixedPrec(1, 0).to_hashable_tuple(), ('FixedPrec', 1, 0, 12))
    self.assertEqual(FixedPrec(1, 3).to_hashable_tuple(), ('FixedPrec', 1, 3, 12))
    self.assertEqual(FixedPrec(1003, 3).to_hashable_tuple(), ('FixedPrec', 1003, 3, 12))
    self.assertEqual(FixedPrec(1000, 3).to_hashable_tuple(), ('FixedPrec', 1000, 3, 12))
    self.assertEqual(FixedPrec(-1, -3).to_hashable_tuple(), ('FixedPrec', -1, -3, 12))
    self.assertEqual(FixedPrec(-1, 0).to_hashable_tuple(), ('FixedPrec', -1, 0, 12))
    self.assertEqual(FixedPrec(-1, 3).to_hashable_tuple(), ('FixedPrec', -1, 3, 12))
    self.assertEqual(FixedPrec(-1003, 3).to_hashable_tuple(), ('FixedPrec', -1003, 3, 12))
    self.assertEqual(FixedPrec(-1000, 3).to_hashable_tuple(), ('FixedPrec', -1000, 3, 12))
  
  def test_from_basic(self):
    self.assertEqual(FixedPrec.from_basic(3).to_hashable_tuple(), FixedPrec(3, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(0).to_hashable_tuple(), FixedPrec(0, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(-3).to_hashable_tuple(), FixedPrec(-3, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(3.0).to_hashable_tuple(), FixedPrec(3_000_000_000_000_000, 15).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(-3.0).to_hashable_tuple(), FixedPrec(-3_000_000_000_000_000, 15).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(30.0).to_hashable_tuple(), FixedPrec(3_000_000_000_000_000, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(0.003).to_hashable_tuple(), FixedPrec(3_000_000_000_000_000, 18).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(1.0).to_hashable_tuple(), FixedPrec(1_000_000_000_000_000, 15).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(0.01).to_hashable_tuple(), FixedPrec(1_000_000_000_000_000, 17).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(-0.01).to_hashable_tuple(), FixedPrec(-1_000_000_000_000_000, 17).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(35.67).to_hashable_tuple(), FixedPrec(3_567_000_000_000_000, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(35.67123456123456).to_hashable_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(-35.67123456123456).to_hashable_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(35.671234561234564).to_hashable_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic(-35.671234561234564).to_hashable_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('0').to_hashable_tuple(), FixedPrec(0, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-0').to_hashable_tuple(), FixedPrec(0, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('1').to_hashable_tuple(), FixedPrec(1, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-1').to_hashable_tuple(), FixedPrec(-1, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('13').to_hashable_tuple(), FixedPrec(13, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-13').to_hashable_tuple(), FixedPrec(-13, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('0.0').to_hashable_tuple(), FixedPrec(0, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-0.0').to_hashable_tuple(), FixedPrec(0, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('1.0').to_hashable_tuple(), FixedPrec(10, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('0.1').to_hashable_tuple(), FixedPrec(1, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-1.0').to_hashable_tuple(), FixedPrec(-10, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-0.1').to_hashable_tuple(), FixedPrec(-1, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('0.01').to_hashable_tuple(), FixedPrec(1, 2).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-0.01').to_hashable_tuple(), FixedPrec(-1, 2).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('10.01').to_hashable_tuple(), FixedPrec(1001, 2).to_hashable_tuple())
    self.assertEqual(FixedPrec.from_basic('-10.01').to_hashable_tuple(), FixedPrec(-1001, 2).to_hashable_tuple())
  
  def test_from_basic_main_constructor(self):
    self.assertEqual(FixedPrec(3).to_hashable_tuple(), FixedPrec(3, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec(0).to_hashable_tuple(), FixedPrec(0, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec(-3).to_hashable_tuple(), FixedPrec(-3, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec(3.0).to_hashable_tuple(), FixedPrec(3_000_000_000_000_000, 15).to_hashable_tuple())
    self.assertEqual(FixedPrec(-3.0).to_hashable_tuple(), FixedPrec(-3_000_000_000_000_000, 15).to_hashable_tuple())
    self.assertEqual(FixedPrec(30.0).to_hashable_tuple(), FixedPrec(3_000_000_000_000_000, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec(0.003).to_hashable_tuple(), FixedPrec(3_000_000_000_000_000, 18).to_hashable_tuple())
    self.assertEqual(FixedPrec(1.0).to_hashable_tuple(), FixedPrec(1_000_000_000_000_000, 15).to_hashable_tuple())
    self.assertEqual(FixedPrec(0.01).to_hashable_tuple(), FixedPrec(1_000_000_000_000_000, 17).to_hashable_tuple())
    self.assertEqual(FixedPrec(-0.01).to_hashable_tuple(), FixedPrec(-1_000_000_000_000_000, 17).to_hashable_tuple())
    self.assertEqual(FixedPrec(35.67).to_hashable_tuple(), FixedPrec(3_567_000_000_000_000, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec(35.67123456123456).to_hashable_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec(-35.67123456123456).to_hashable_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec(35.671234561234564).to_hashable_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec(-35.671234561234564).to_hashable_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_hashable_tuple())
    self.assertEqual(FixedPrec('0').to_hashable_tuple(), FixedPrec(0, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec('-0').to_hashable_tuple(), FixedPrec(0, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec('1').to_hashable_tuple(), FixedPrec(1, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec('-1').to_hashable_tuple(), FixedPrec(-1, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec('13').to_hashable_tuple(), FixedPrec(13, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec('-13').to_hashable_tuple(), FixedPrec(-13, 0).to_hashable_tuple())
    self.assertEqual(FixedPrec('0.0').to_hashable_tuple(), FixedPrec(0, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec('-0.0').to_hashable_tuple(), FixedPrec(0, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec('1.0').to_hashable_tuple(), FixedPrec(10, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec('0.1').to_hashable_tuple(), FixedPrec(1, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec('-1.0').to_hashable_tuple(), FixedPrec(-10, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec('-0.1').to_hashable_tuple(), FixedPrec(-1, 1).to_hashable_tuple())
    self.assertEqual(FixedPrec('0.01').to_hashable_tuple(), FixedPrec(1, 2).to_hashable_tuple())
    self.assertEqual(FixedPrec('-0.01').to_hashable_tuple(), FixedPrec(-1, 2).to_hashable_tuple())
    self.assertEqual(FixedPrec('10.01').to_hashable_tuple(), FixedPrec(1001, 2).to_hashable_tuple())
    self.assertEqual(FixedPrec('-10.01').to_hashable_tuple(), FixedPrec(-1001, 2).to_hashable_tuple())
  
  def test_auto_casting(self):
    self.assertEqual(FixedPrec.from_basic(3) + 5, 8)
    self.assertEqual(FixedPrec.from_basic(3) - 5, -2)
    self.assertEqual(FixedPrec.from_basic(3) > 5, False)
    self.assertEqual(FixedPrec.from_basic(3) < 5, True)
    self.assertEqual(FixedPrec.from_basic(3) * -4, -12)
  
  def test_op_errors(self):
    self.assertEqual(FixedPrec.from_basic(FixedPrec(3), cast_only = True), FixedPrec(3))
    
    with self.assertRaises(NotImplementedError):
      FixedPrec.from_basic('3', cast_only = True)
    
    with self.assertRaises(TypeError):
      FixedPrec(3) + '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) - '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) * '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) // '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) % '4'
    
    with self.assertRaises(TypeError):
      divmod(FixedPrec(3), '4')
    
    with self.assertRaises(TypeError):
      '4' + FixedPrec(3)
    
    with self.assertRaises(TypeError):
      '4' - FixedPrec(3)
    
    with self.assertRaises(TypeError):
      '4' * FixedPrec(3)
    
    self.assertEqual(FixedPrec(4) == '4', False)
    self.assertEqual(FixedPrec(4) != '4', True)
    
    with self.assertRaises(TypeError):
      FixedPrec(3) > '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) < '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) >= '4'
    
    with self.assertRaises(TypeError):
      FixedPrec(3) <= '4'
    
    self.assertEqual('4' == FixedPrec(4), False)
    self.assertEqual('4' != FixedPrec(4), True)
    
    with self.assertRaises(TypeError):
      '4' > FixedPrec(3)
    
    with self.assertRaises(TypeError):
      '4' < FixedPrec(3)
    
    with self.assertRaises(TypeError):
      '4' >= FixedPrec(3)
    
    with self.assertRaises(TypeError):
      '4' <= FixedPrec(3)
