import unittest

from ..fixed_prec import FixedPrec

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
  
  def test_neg(self):
    self.assertEqual(str(-FixedPrec(1, 0)), '-1')
    self.assertEqual(str(-FixedPrec(0, 0)), '0')
  
  def test_add(self):
    self.assertEqual(str(FixedPrec(1, 0) + FixedPrec(3, 0)), '4')
    self.assertEqual(str(FixedPrec(1, 0) + FixedPrec(3, 3)), '1.003')
    self.assertEqual(str(FixedPrec(1, 0) + FixedPrec(3, -3)), '3001')
    self.assertEqual(str(FixedPrec(1, 0) - FixedPrec(3, 0)), '-2')
    self.assertEqual(str(FixedPrec(1, 0) - FixedPrec(3, 3)), '0.997')
    self.assertEqual(str(FixedPrec(1, 0) - FixedPrec(3, -3)), '-2999')
  
  def test_mul(self):
    self.assertEqual(str(FixedPrec(1, 0) * FixedPrec(3, 0)), '3')
    self.assertEqual(str(FixedPrec(8, 0) * FixedPrec(12, 0)), '96')
    self.assertEqual(str(FixedPrec(8, 0) * FixedPrec(12, 1)), '9.6')
    self.assertEqual(str(FixedPrec(8, 1) * FixedPrec(12, 1)), '0.96')
    self.assertEqual(str(FixedPrec(8, 1) * FixedPrec(12, 20)), '0.000000000000')
  
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
  
  def test_auto_casting(self):
    self.assertEqual(FixedPrec.from_basic(3) + 5, 8)
    self.assertEqual(FixedPrec.from_basic(3) - 5, -2)
    self.assertEqual(FixedPrec.from_basic(3) > 5, False)
    self.assertEqual(FixedPrec.from_basic(3) < 5, True)
    self.assertEqual(FixedPrec.from_basic(3) * -4, -12)
