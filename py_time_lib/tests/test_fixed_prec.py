from math import floor, ceil, trunc
import unittest

from .. import FixedPrec

class TestFixedPrec(unittest.TestCase):
  def test_repr(self):
    self.assertEqual(repr(FixedPrec(0, -3)), 'FixedPrec(0)')
    self.assertEqual(repr(FixedPrec(0, 0)), 'FixedPrec(0)')
    self.assertEqual(repr(FixedPrec(0, 3)), "FixedPrec('0.000')")
    self.assertEqual(repr(FixedPrec(1, -3)), 'FixedPrec(1000)')
    self.assertEqual(repr(FixedPrec(1, 0)), 'FixedPrec(1)')
    self.assertEqual(repr(FixedPrec(1, 3)), "FixedPrec('0.001')")
    self.assertEqual(repr(FixedPrec(1003, 3)), "FixedPrec('1.003')")
    self.assertEqual(repr(FixedPrec(1000, 3)), "FixedPrec('1.000')")
    self.assertEqual(repr(FixedPrec(-1, -3)), 'FixedPrec(-1000)')
    self.assertEqual(repr(FixedPrec(-1, 0)), 'FixedPrec(-1)')
    self.assertEqual(repr(FixedPrec(-1, 3)), "FixedPrec('-0.001')")
    self.assertEqual(repr(FixedPrec(-1003, 3)), "FixedPrec('-1.003')")
    self.assertEqual(repr(FixedPrec(-1000, 3)), "FixedPrec('-1.000')")
  
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
    
    self.assertEqual((FixedPrec(3) + 5).to_data_tuple(), ('FixedPrec', 8, 0, 12))
    self.assertEqual((5 + FixedPrec(3)).to_data_tuple(), ('FixedPrec', 8, 0, 12))
  
  def test_mul(self):
    self.assertEqual(str(FixedPrec(1, 0) * FixedPrec(3, 0)), '3')
    self.assertEqual(str(FixedPrec(8, 0) * FixedPrec(12, 0)), '96')
    self.assertEqual(str(FixedPrec(8, 0) * FixedPrec(12, 1)), '9.6')
    self.assertEqual(str(FixedPrec(8, 1) * FixedPrec(12, 1)), '0.96')
    self.assertEqual(str(FixedPrec(8, 1) * FixedPrec(12, 20)), '0.000000000000')
    
    self.assertEqual((FixedPrec(3) * 5).to_data_tuple(), ('FixedPrec', 15, 0, 12))
    self.assertEqual((5 * FixedPrec(3)).to_data_tuple(), ('FixedPrec', 15, 0, 12))
  
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
    
    self.assertEqual((FixedPrec(11) // 3).to_data_tuple(), ('FixedPrec', 3, 0, 12))
    self.assertEqual((11 // FixedPrec(3)).to_data_tuple(), ('FixedPrec', 3, 0, 12))
    
    self.assertEqual((FixedPrec(11) % 3).to_data_tuple(), ('FixedPrec', 2, 0, 12))
    self.assertEqual((11 % FixedPrec(3)).to_data_tuple(), ('FixedPrec', 2, 0, 12))
    
    self.assertEqual(tuple(x.to_data_tuple() for x in divmod(FixedPrec(11), 3)), (('FixedPrec', 3, 0, 12), ('FixedPrec', 2, 0, 12)))
    self.assertEqual(tuple(x.to_data_tuple() for x in divmod(11, FixedPrec(3))), (('FixedPrec', 3, 0, 12), ('FixedPrec', 2, 0, 12)))
  
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
    
    self.assertEqual((FixedPrec(12) / 3).to_data_tuple(), ('FixedPrec', 4_000_000_000_000, 12, 12))
    self.assertEqual((12 / FixedPrec(3)).to_data_tuple(), ('FixedPrec', 4_000_000_000_000, 12, 12))
    
    self.assertAlmostEqual(FixedPrec(1) / FixedPrec('1.999999999996'), FixedPrec('0.5'), delta = 1e-12)
    self.assertAlmostEqual(FixedPrec(2) / FixedPrec('1.999999999996'), 1, delta = 1e-11)
    self.assertAlmostEqual(FixedPrec(1) / 1.999999999996, FixedPrec('0.5'), delta = 1e-12)
    self.assertAlmostEqual(FixedPrec(2) / 1.999999999996, 1, delta = 1e-11)
    self.assertAlmostEqual(1 / FixedPrec('1.999999999996'), FixedPrec('0.5'), delta = 1e-12)
    self.assertAlmostEqual(2 / FixedPrec('1.999999999996'), 1, delta = 1e-11)
  
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
  
  def test_to_data_tuple(self):
    self.assertEqual(FixedPrec(0, -3).to_data_tuple(), ('FixedPrec', 0, -3, 12))
    self.assertEqual(FixedPrec(0, 0).to_data_tuple(), ('FixedPrec', 0, 0, 12))
    self.assertEqual(FixedPrec(0, 3).to_data_tuple(), ('FixedPrec', 0, 3, 12))
    self.assertEqual(FixedPrec(1, -3).to_data_tuple(), ('FixedPrec', 1, -3, 12))
    self.assertEqual(FixedPrec(1, 0).to_data_tuple(), ('FixedPrec', 1, 0, 12))
    self.assertEqual(FixedPrec(1, 3).to_data_tuple(), ('FixedPrec', 1, 3, 12))
    self.assertEqual(FixedPrec(1003, 3).to_data_tuple(), ('FixedPrec', 1003, 3, 12))
    self.assertEqual(FixedPrec(1000, 3).to_data_tuple(), ('FixedPrec', 1000, 3, 12))
    self.assertEqual(FixedPrec(-1, -3).to_data_tuple(), ('FixedPrec', -1, -3, 12))
    self.assertEqual(FixedPrec(-1, 0).to_data_tuple(), ('FixedPrec', -1, 0, 12))
    self.assertEqual(FixedPrec(-1, 3).to_data_tuple(), ('FixedPrec', -1, 3, 12))
    self.assertEqual(FixedPrec(-1003, 3).to_data_tuple(), ('FixedPrec', -1003, 3, 12))
    self.assertEqual(FixedPrec(-1000, 3).to_data_tuple(), ('FixedPrec', -1000, 3, 12))
  
  def test_to_hashable_tuple(self):
    self.assertEqual(FixedPrec(0, -3).to_hashable_tuple(), ('FixedPrec', 0, -3))
    self.assertEqual(FixedPrec(0, 0).to_hashable_tuple(), ('FixedPrec', 0, 0))
    self.assertEqual(FixedPrec(0, 3).to_hashable_tuple(), ('FixedPrec', 0, 3))
    self.assertEqual(FixedPrec(1, -3).to_hashable_tuple(), ('FixedPrec', 1, -3))
    self.assertEqual(FixedPrec(1, 0).to_hashable_tuple(), ('FixedPrec', 1, 0))
    self.assertEqual(FixedPrec(1, 3).to_hashable_tuple(), ('FixedPrec', 1, 3))
    self.assertEqual(FixedPrec(1003, 3).to_hashable_tuple(), ('FixedPrec', 1003, 3))
    self.assertEqual(FixedPrec(1000, 3).to_hashable_tuple(), ('FixedPrec', 1000, 3))
    self.assertEqual(FixedPrec(-1, -3).to_hashable_tuple(), ('FixedPrec', -1, -3))
    self.assertEqual(FixedPrec(-1, 0).to_hashable_tuple(), ('FixedPrec', -1, 0))
    self.assertEqual(FixedPrec(-1, 3).to_hashable_tuple(), ('FixedPrec', -1, 3))
    self.assertEqual(FixedPrec(-1003, 3).to_hashable_tuple(), ('FixedPrec', -1003, 3))
    self.assertEqual(FixedPrec(-1000, 3).to_hashable_tuple(), ('FixedPrec', -1000, 3))
  
  def test_from_basic(self):
    self.assertEqual(FixedPrec.from_basic(3).to_data_tuple(), FixedPrec(3, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(0).to_data_tuple(), FixedPrec(0, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(-3).to_data_tuple(), FixedPrec(-3, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(3.0).to_data_tuple(), FixedPrec(3_000_000_000_000_000, 15).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(0.0).to_data_tuple(), FixedPrec(0, 15).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(-3.0).to_data_tuple(), FixedPrec(-3_000_000_000_000_000, 15).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(30.0).to_data_tuple(), FixedPrec(3_000_000_000_000_000, 14).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(0.003).to_data_tuple(), FixedPrec(3_000_000_000_000_000, 18).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(1.0).to_data_tuple(), FixedPrec(1_000_000_000_000_000, 15).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(0.01).to_data_tuple(), FixedPrec(1_000_000_000_000_000, 17).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(-0.01).to_data_tuple(), FixedPrec(-1_000_000_000_000_000, 17).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(35.67).to_data_tuple(), FixedPrec(3_567_000_000_000_000, 14).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(35.67123456123456).to_data_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(-35.67123456123456).to_data_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(35.671234561234564).to_data_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic(-35.671234561234564).to_data_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('0').to_data_tuple(), FixedPrec(0, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-0').to_data_tuple(), FixedPrec(0, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('1').to_data_tuple(), FixedPrec(1, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-1').to_data_tuple(), FixedPrec(-1, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('13').to_data_tuple(), FixedPrec(13, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-13').to_data_tuple(), FixedPrec(-13, 0).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('0.0').to_data_tuple(), FixedPrec(0, 1).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-0.0').to_data_tuple(), FixedPrec(0, 1).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('1.0').to_data_tuple(), FixedPrec(10, 1).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('0.1').to_data_tuple(), FixedPrec(1, 1).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-1.0').to_data_tuple(), FixedPrec(-10, 1).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-0.1').to_data_tuple(), FixedPrec(-1, 1).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('0.01').to_data_tuple(), FixedPrec(1, 2).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-0.01').to_data_tuple(), FixedPrec(-1, 2).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('10.01').to_data_tuple(), FixedPrec(1001, 2).to_data_tuple())
    self.assertEqual(FixedPrec.from_basic('-10.01').to_data_tuple(), FixedPrec(-1001, 2).to_data_tuple())
  
  def test_from_basic_main_constructor(self):
    self.assertEqual(FixedPrec(3).to_data_tuple(), FixedPrec(3, 0).to_data_tuple())
    self.assertEqual(FixedPrec(0).to_data_tuple(), FixedPrec(0, 0).to_data_tuple())
    self.assertEqual(FixedPrec(-3).to_data_tuple(), FixedPrec(-3, 0).to_data_tuple())
    self.assertEqual(FixedPrec(3.0).to_data_tuple(), FixedPrec(3_000_000_000_000_000, 15).to_data_tuple())
    self.assertEqual(FixedPrec(-3.0).to_data_tuple(), FixedPrec(-3_000_000_000_000_000, 15).to_data_tuple())
    self.assertEqual(FixedPrec(30.0).to_data_tuple(), FixedPrec(3_000_000_000_000_000, 14).to_data_tuple())
    self.assertEqual(FixedPrec(0.003).to_data_tuple(), FixedPrec(3_000_000_000_000_000, 18).to_data_tuple())
    self.assertEqual(FixedPrec(1.0).to_data_tuple(), FixedPrec(1_000_000_000_000_000, 15).to_data_tuple())
    self.assertEqual(FixedPrec(0.01).to_data_tuple(), FixedPrec(1_000_000_000_000_000, 17).to_data_tuple())
    self.assertEqual(FixedPrec(-0.01).to_data_tuple(), FixedPrec(-1_000_000_000_000_000, 17).to_data_tuple())
    self.assertEqual(FixedPrec(35.67).to_data_tuple(), FixedPrec(3_567_000_000_000_000, 14).to_data_tuple())
    self.assertEqual(FixedPrec(35.67123456123456).to_data_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec(-35.67123456123456).to_data_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec(35.671234561234564).to_data_tuple(), FixedPrec(3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec(-35.671234561234564).to_data_tuple(), FixedPrec(-3_567_123_456_123_456, 14).to_data_tuple())
    self.assertEqual(FixedPrec('0').to_data_tuple(), FixedPrec(0, 0).to_data_tuple())
    self.assertEqual(FixedPrec('-0').to_data_tuple(), FixedPrec(0, 0).to_data_tuple())
    self.assertEqual(FixedPrec('1').to_data_tuple(), FixedPrec(1, 0).to_data_tuple())
    self.assertEqual(FixedPrec('-1').to_data_tuple(), FixedPrec(-1, 0).to_data_tuple())
    self.assertEqual(FixedPrec('13').to_data_tuple(), FixedPrec(13, 0).to_data_tuple())
    self.assertEqual(FixedPrec('-13').to_data_tuple(), FixedPrec(-13, 0).to_data_tuple())
    self.assertEqual(FixedPrec('0.0').to_data_tuple(), FixedPrec(0, 1).to_data_tuple())
    self.assertEqual(FixedPrec('-0.0').to_data_tuple(), FixedPrec(0, 1).to_data_tuple())
    self.assertEqual(FixedPrec('1.0').to_data_tuple(), FixedPrec(10, 1).to_data_tuple())
    self.assertEqual(FixedPrec('0.1').to_data_tuple(), FixedPrec(1, 1).to_data_tuple())
    self.assertEqual(FixedPrec('-1.0').to_data_tuple(), FixedPrec(-10, 1).to_data_tuple())
    self.assertEqual(FixedPrec('-0.1').to_data_tuple(), FixedPrec(-1, 1).to_data_tuple())
    self.assertEqual(FixedPrec('0.01').to_data_tuple(), FixedPrec(1, 2).to_data_tuple())
    self.assertEqual(FixedPrec('-0.01').to_data_tuple(), FixedPrec(-1, 2).to_data_tuple())
    self.assertEqual(FixedPrec('10.01').to_data_tuple(), FixedPrec(1001, 2).to_data_tuple())
    self.assertEqual(FixedPrec('-10.01').to_data_tuple(), FixedPrec(-1001, 2).to_data_tuple())
  
  def test_auto_casting(self):
    self.assertEqual(FixedPrec.from_basic(3) + 5, 8)
    self.assertEqual(FixedPrec.from_basic(3) - 5, -2)
    self.assertEqual(FixedPrec.from_basic(3) > 5, False)
    self.assertEqual(FixedPrec.from_basic(3) < 5, True)
    self.assertEqual(FixedPrec.from_basic(3) * -4, -12)
  
  def test_op_errors(self):
    self.assertEqual(FixedPrec.from_basic(FixedPrec(3), cast_only = True), FixedPrec(3))
    
    with self.assertRaises(TypeError):
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
  
  def test_complex_abc(self):
    # complex
    
    self.assertEqual(complex(FixedPrec(3)), 3+0j)
    self.assertEqual(complex(FixedPrec(0)), 0j)
    self.assertEqual(complex(FixedPrec(-3)), -3+0j)
    
    # reduce to lowest prec
    
    self.assertEqual(FixedPrec(10, 1).reduce_to_lowest_place().to_data_tuple(), ('FixedPrec', 1, 0, 12))
    self.assertEqual(FixedPrec(12, 1).reduce_to_lowest_place().to_data_tuple(), ('FixedPrec', 12, 1, 12))
    self.assertEqual(FixedPrec(-10, 1).reduce_to_lowest_place().to_data_tuple(), ('FixedPrec', -1, 0, 12))
    self.assertEqual(FixedPrec(-12, 1).reduce_to_lowest_place().to_data_tuple(), ('FixedPrec', -12, 1, 12))
    self.assertEqual(FixedPrec(0, 1).reduce_to_lowest_place().to_data_tuple(), ('FixedPrec', 0, 0, 12))
    self.assertEqual(FixedPrec(0, 0).reduce_to_lowest_place().to_data_tuple(), ('FixedPrec', 0, 0, 12))
    
    # pow 1 & 0 base
    self.assertEqual(FixedPrec(1) ** FixedPrec(0), 1)
    self.assertEqual(FixedPrec(1) ** FixedPrec(1), 1)
    self.assertEqual(FixedPrec(1) ** FixedPrec(2), 1)
    self.assertEqual(FixedPrec(1) ** FixedPrec(1024), 1)
    self.assertEqual(FixedPrec(0) ** FixedPrec(0), 1)
    self.assertEqual(FixedPrec(0) ** FixedPrec(1), 0)
    self.assertEqual(FixedPrec(0) ** FixedPrec(2), 0)
    self.assertEqual(FixedPrec(0) ** FixedPrec(1024), 0)
    with self.assertRaises(ZeroDivisionError):
      FixedPrec(0) ** FixedPrec('-1')
    with self.assertRaises(ZeroDivisionError):
      FixedPrec(0) ** FixedPrec('-2')
    with self.assertRaises(ZeroDivisionError):
      FixedPrec(0) ** FixedPrec('-1024')
    
    # pow positive int exponent
    self.assertEqual(FixedPrec(3) ** FixedPrec(0), 1)
    self.assertEqual(FixedPrec(3) ** FixedPrec(1), 3)
    self.assertEqual(FixedPrec(3) ** FixedPrec(2), 9)
    self.assertEqual(FixedPrec(3) ** FixedPrec(3), 27)
    self.assertEqual(FixedPrec(3) ** FixedPrec(4), 81)
    self.assertEqual(FixedPrec(3) ** FixedPrec(5), 3 ** 5)
    self.assertEqual(FixedPrec(3) ** FixedPrec(6), 3 ** 6)
    self.assertEqual(FixedPrec(3) ** FixedPrec(7), 3 ** 7)
    self.assertEqual(FixedPrec(3) ** FixedPrec(8), 3 ** 8)
    self.assertEqual(FixedPrec(3) ** FixedPrec(9), 3 ** 9)
    self.assertEqual(FixedPrec(3) ** FixedPrec(10), 3 ** 10)
    self.assertEqual(FixedPrec(3) ** FixedPrec(11), 3 ** 11)
    
    # nthroot
    
    self.assertEqual(FixedPrec(4)._nthroot(1), 4)
    self.assertEqual(FixedPrec(9)._nthroot(1), 9)
    self.assertEqual(FixedPrec(1)._nthroot(1), 1)
    self.assertEqual(FixedPrec(1)._nthroot(2), 1)
    self.assertEqual(FixedPrec(1)._nthroot(10), 1)
    self.assertEqual(FixedPrec(4)._nthroot(2), 2)
    self.assertEqual(FixedPrec(9)._nthroot(2), 3)
    self.assertEqual(FixedPrec(16)._nthroot(2), 4)
    self.assertEqual(FixedPrec(16)._nthroot(4), 2)
    self.assertAlmostEqual(FixedPrec('0.25')._nthroot(2), FixedPrec('0.5'), delta = 1e-12)
    self.assertAlmostEqual(FixedPrec('0.0625')._nthroot(2), FixedPrec('0.25'), delta = 1e-12)
    self.assertAlmostEqual(FixedPrec('0.0625')._nthroot(4), FixedPrec('0.5'), delta = 1e-12)
    
    # pow positive fractional exponent
    
    self.assertEqual(FixedPrec(4) ** FixedPrec(0), 1)
    self.assertAlmostEqual(FixedPrec(4) ** FixedPrec('0.5'), 2, delta = 1e-11)
    self.assertEqual(FixedPrec(4) ** FixedPrec(1), 4)
    self.assertAlmostEqual(FixedPrec(4) ** FixedPrec('1.5'), 8, delta = 1e-10)
    self.assertEqual(FixedPrec(4) ** FixedPrec(2), 16)
    
    # pow negative fractional exponent
    
    self.assertAlmostEqual(FixedPrec(4) ** FixedPrec('-0.5'), FixedPrec('0.5'), delta = 1e-12)
    self.assertEqual(FixedPrec(4) ** FixedPrec(-1), FixedPrec('0.25'))
    self.assertEqual(FixedPrec(4) ** FixedPrec('-1.5'), FixedPrec('0.125'))
    self.assertEqual(FixedPrec(4) ** FixedPrec(-2), FixedPrec('0.0625'))
    self.assertEqual(FixedPrec(-4) ** FixedPrec(2), 16)
    self.assertEqual(FixedPrec(-4) ** FixedPrec(-2), FixedPrec('0.0625'))
    self.assertEqual(FixedPrec(-4) ** FixedPrec(3), -64)
    self.assertEqual(FixedPrec(-4) ** FixedPrec(-3), FixedPrec('-0.015625'))
    with self.assertRaises(ValueError):
      FixedPrec(-4) ** FixedPrec('0.5')
    with self.assertRaises(ValueError):
      FixedPrec(-4) ** FixedPrec('1.5')
    with self.assertRaises(ValueError):
      FixedPrec(-4) ** FixedPrec('-0.5')
    with self.assertRaises(ValueError):
      FixedPrec(-4) ** FixedPrec('-1.5')
    
    # pow type coercion & rpow
    
    self.assertEqual(FixedPrec(4) ** -1.5, FixedPrec('0.125'))
    self.assertEqual(4 ** FixedPrec('-1.5'), FixedPrec('0.125'))
    
    # conjugate
    
    self.assertEqual(FixedPrec(4).conjugate(), 4)
    self.assertEqual(FixedPrec(0).conjugate(), 0)
    self.assertEqual(FixedPrec(-4).conjugate(), -4)
    
    # real
    
    self.assertEqual(FixedPrec(4).real, 4)
    self.assertEqual(FixedPrec(0).real, 0)
    self.assertEqual(FixedPrec(-4).real, -4)
    
    # imag
    
    self.assertEqual(FixedPrec(4).imag, 0)
    self.assertEqual(FixedPrec(0).imag, 0)
    self.assertEqual(FixedPrec(-4).imag, 0)
  
  def test_real_abc(self):
    # floor
    
    self.assertEqual(floor(FixedPrec(17, 0)), FixedPrec(17))
    self.assertEqual(floor(FixedPrec(15, 0)), FixedPrec(15))
    self.assertEqual(floor(FixedPrec(13, 0)), FixedPrec(13))
    self.assertEqual(floor(FixedPrec(0, 0)), FixedPrec(0))
    self.assertEqual(floor(FixedPrec(-13, 0)), FixedPrec(-13))
    self.assertEqual(floor(FixedPrec(-15, 0)), FixedPrec(-15))
    self.assertEqual(floor(FixedPrec(-17, 0)), FixedPrec(-17))
    
    self.assertEqual(floor(FixedPrec(17, 1)), FixedPrec(1))
    self.assertEqual(floor(FixedPrec(15, 1)), FixedPrec(1))
    self.assertEqual(floor(FixedPrec(13, 1)), FixedPrec(1))
    self.assertEqual(floor(FixedPrec(0, 1)), FixedPrec(0))
    self.assertEqual(floor(FixedPrec(-13, 1)), FixedPrec(-2))
    self.assertEqual(floor(FixedPrec(-15, 1)), FixedPrec(-2))
    self.assertEqual(floor(FixedPrec(-17, 1)), FixedPrec(-2))
    
    self.assertEqual(floor(FixedPrec(17, -1)), FixedPrec(170))
    self.assertEqual(floor(FixedPrec(15, -1)), FixedPrec(150))
    self.assertEqual(floor(FixedPrec(13, -1)), FixedPrec(130))
    self.assertEqual(floor(FixedPrec(0, -1)), FixedPrec(0))
    self.assertEqual(floor(FixedPrec(-13, -1)), FixedPrec(-130))
    self.assertEqual(floor(FixedPrec(-15, -1)), FixedPrec(-150))
    self.assertEqual(floor(FixedPrec(-17, -1)), FixedPrec(-170))
    
    # ceil
    
    self.assertEqual(ceil(FixedPrec(17, 0)), FixedPrec(17))
    self.assertEqual(ceil(FixedPrec(15, 0)), FixedPrec(15))
    self.assertEqual(ceil(FixedPrec(13, 0)), FixedPrec(13))
    self.assertEqual(ceil(FixedPrec(0, 0)), FixedPrec(0))
    self.assertEqual(ceil(FixedPrec(-13, 0)), FixedPrec(-13))
    self.assertEqual(ceil(FixedPrec(-15, 0)), FixedPrec(-15))
    self.assertEqual(ceil(FixedPrec(-17, 0)), FixedPrec(-17))
    
    self.assertEqual(ceil(FixedPrec(17, 1)), FixedPrec(2))
    self.assertEqual(ceil(FixedPrec(15, 1)), FixedPrec(2))
    self.assertEqual(ceil(FixedPrec(13, 1)), FixedPrec(2))
    self.assertEqual(ceil(FixedPrec(0, 1)), FixedPrec(0))
    self.assertEqual(ceil(FixedPrec(-13, 1)), FixedPrec(-1))
    self.assertEqual(ceil(FixedPrec(-15, 1)), FixedPrec(-1))
    self.assertEqual(ceil(FixedPrec(-17, 1)), FixedPrec(-1))
    
    self.assertEqual(ceil(FixedPrec(17, -1)), FixedPrec(170))
    self.assertEqual(ceil(FixedPrec(15, -1)), FixedPrec(150))
    self.assertEqual(ceil(FixedPrec(13, -1)), FixedPrec(130))
    self.assertEqual(ceil(FixedPrec(0, -1)), FixedPrec(0))
    self.assertEqual(ceil(FixedPrec(-13, -1)), FixedPrec(-130))
    self.assertEqual(ceil(FixedPrec(-15, -1)), FixedPrec(-150))
    self.assertEqual(ceil(FixedPrec(-17, -1)), FixedPrec(-170))
    
    # trunc
    
    self.assertEqual(trunc(FixedPrec(17, 0)), FixedPrec(17))
    self.assertEqual(trunc(FixedPrec(15, 0)), FixedPrec(15))
    self.assertEqual(trunc(FixedPrec(13, 0)), FixedPrec(13))
    self.assertEqual(trunc(FixedPrec(0, 0)), FixedPrec(0))
    self.assertEqual(trunc(FixedPrec(-13, 0)), FixedPrec(-13))
    self.assertEqual(trunc(FixedPrec(-15, 0)), FixedPrec(-15))
    self.assertEqual(trunc(FixedPrec(-17, 0)), FixedPrec(-17))
    
    self.assertEqual(trunc(FixedPrec(17, 1)), FixedPrec(1))
    self.assertEqual(trunc(FixedPrec(15, 1)), FixedPrec(1))
    self.assertEqual(trunc(FixedPrec(13, 1)), FixedPrec(1))
    self.assertEqual(trunc(FixedPrec(0, 1)), FixedPrec(0))
    self.assertEqual(trunc(FixedPrec(-13, 1)), FixedPrec(-1))
    self.assertEqual(trunc(FixedPrec(-15, 1)), FixedPrec(-1))
    self.assertEqual(trunc(FixedPrec(-17, 1)), FixedPrec(-1))
    
    self.assertEqual(trunc(FixedPrec(17, -1)), FixedPrec(170))
    self.assertEqual(trunc(FixedPrec(15, -1)), FixedPrec(150))
    self.assertEqual(trunc(FixedPrec(13, -1)), FixedPrec(130))
    self.assertEqual(trunc(FixedPrec(0, -1)), FixedPrec(0))
    self.assertEqual(trunc(FixedPrec(-13, -1)), FixedPrec(-130))
    self.assertEqual(trunc(FixedPrec(-15, -1)), FixedPrec(-150))
    self.assertEqual(trunc(FixedPrec(-17, -1)), FixedPrec(-170))
    
    # round
    
    self.assertEqual(round(FixedPrec(17, 0)), FixedPrec(17))
    self.assertEqual(round(FixedPrec(15, 0)), FixedPrec(15))
    self.assertEqual(round(FixedPrec(13, 0)), FixedPrec(13))
    self.assertEqual(round(FixedPrec(0, 0)), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 0)), FixedPrec(-13))
    self.assertEqual(round(FixedPrec(-15, 0)), FixedPrec(-15))
    self.assertEqual(round(FixedPrec(-17, 0)), FixedPrec(-17))
    
    self.assertEqual(round(FixedPrec(17, 1)), FixedPrec(2))
    self.assertEqual(round(FixedPrec(15, 1)), FixedPrec(2))
    self.assertEqual(round(FixedPrec(13, 1)), FixedPrec(1))
    self.assertEqual(round(FixedPrec(0, 1)), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 1)), FixedPrec(-1))
    self.assertEqual(round(FixedPrec(-15, 1)), FixedPrec(-1))
    self.assertEqual(round(FixedPrec(-17, 1)), FixedPrec(-2))
    
    self.assertEqual(round(FixedPrec(17, -1)), FixedPrec(170))
    self.assertEqual(round(FixedPrec(15, -1)), FixedPrec(150))
    self.assertEqual(round(FixedPrec(13, -1)), FixedPrec(130))
    self.assertEqual(round(FixedPrec(0, -1)), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, -1)), FixedPrec(-130))
    self.assertEqual(round(FixedPrec(-15, -1)), FixedPrec(-150))
    self.assertEqual(round(FixedPrec(-17, -1)), FixedPrec(-170))
    
    # round 1 digit
    
    self.assertEqual(round(FixedPrec(17, 0), 1), FixedPrec(17))
    self.assertEqual(round(FixedPrec(15, 0), 1), FixedPrec(15))
    self.assertEqual(round(FixedPrec(13, 0), 1), FixedPrec(13))
    self.assertEqual(round(FixedPrec(0, 0), 1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 0), 1), FixedPrec(-13))
    self.assertEqual(round(FixedPrec(-15, 0), 1), FixedPrec(-15))
    self.assertEqual(round(FixedPrec(-17, 0), 1), FixedPrec(-17))
    
    self.assertEqual(round(FixedPrec(17, 1), 1), FixedPrec('1.7'))
    self.assertEqual(round(FixedPrec(15, 1), 1), FixedPrec('1.5'))
    self.assertEqual(round(FixedPrec(13, 1), 1), FixedPrec('1.3'))
    self.assertEqual(round(FixedPrec(0, 1), 1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 1), 1), FixedPrec('-1.3'))
    self.assertEqual(round(FixedPrec(-15, 1), 1), FixedPrec('-1.5'))
    self.assertEqual(round(FixedPrec(-17, 1), 1), FixedPrec('-1.7'))
    
    self.assertEqual(round(FixedPrec(17, 2), 1), FixedPrec('0.2'))
    self.assertEqual(round(FixedPrec(15, 2), 1), FixedPrec('0.2'))
    self.assertEqual(round(FixedPrec(13, 2), 1), FixedPrec('0.1'))
    self.assertEqual(round(FixedPrec(0, 2), 1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 2), 1), FixedPrec('-0.1'))
    self.assertEqual(round(FixedPrec(-15, 2), 1), FixedPrec('-0.1'))
    self.assertEqual(round(FixedPrec(-17, 2), 1), FixedPrec('-0.2'))
    
    self.assertEqual(round(FixedPrec(17, -1), 1), FixedPrec(170))
    self.assertEqual(round(FixedPrec(15, -1), 1), FixedPrec(150))
    self.assertEqual(round(FixedPrec(13, -1), 1), FixedPrec(130))
    self.assertEqual(round(FixedPrec(0, -1), 1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, -1), 1), FixedPrec(-130))
    self.assertEqual(round(FixedPrec(-15, -1), 1), FixedPrec(-150))
    self.assertEqual(round(FixedPrec(-17, -1), 1), FixedPrec(-170))
    
    # round -1 digit
    
    self.assertEqual(round(FixedPrec(17, 0), -1), FixedPrec(20))
    self.assertEqual(round(FixedPrec(15, 0), -1), FixedPrec(20))
    self.assertEqual(round(FixedPrec(13, 0), -1), FixedPrec(10))
    self.assertEqual(round(FixedPrec(0, 0), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 0), -1), FixedPrec(-10))
    self.assertEqual(round(FixedPrec(-15, 0), -1), FixedPrec(-10))
    self.assertEqual(round(FixedPrec(-17, 0), -1), FixedPrec(-20))
    
    self.assertEqual(round(FixedPrec(17, 1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(15, 1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(13, 1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(0, 1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, 1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-15, 1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-17, 1), -1), FixedPrec(0))
    
    self.assertEqual(round(FixedPrec(17, -1), -1), FixedPrec(170))
    self.assertEqual(round(FixedPrec(15, -1), -1), FixedPrec(150))
    self.assertEqual(round(FixedPrec(13, -1), -1), FixedPrec(130))
    self.assertEqual(round(FixedPrec(0, -1), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, -1), -1), FixedPrec(-130))
    self.assertEqual(round(FixedPrec(-15, -1), -1), FixedPrec(-150))
    self.assertEqual(round(FixedPrec(-17, -1), -1), FixedPrec(-170))
    
    self.assertEqual(round(FixedPrec(17, -2), -1), FixedPrec(1700))
    self.assertEqual(round(FixedPrec(15, -2), -1), FixedPrec(1500))
    self.assertEqual(round(FixedPrec(13, -2), -1), FixedPrec(1300))
    self.assertEqual(round(FixedPrec(0, -2), -1), FixedPrec(0))
    self.assertEqual(round(FixedPrec(-13, -2), -1), FixedPrec(-1300))
    self.assertEqual(round(FixedPrec(-15, -2), -1), FixedPrec(-1500))
    self.assertEqual(round(FixedPrec(-17, -2), -1), FixedPrec(-1700))
  
  def test_hash(self):
    self.assertEqual(hash(FixedPrec(3)), hash(3))
    self.assertEqual(hash(FixedPrec('3.5')), hash(3.5))
    self.assertEqual(hash(FixedPrec('17846517823657823658916666263.5')), hash(('FixedPrec', 178465178236578236589166662635, 1)))
  
  def test_no_attributes(self):
    with self.assertRaises(AttributeError):
      d1 = FixedPrec(2024)
      d1.prop = False
