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
    self.assertEqual(str(FixedPrec(-1, -3)), '-1000')
    self.assertEqual(str(FixedPrec(-1, 0)), '-1')
    self.assertEqual(str(FixedPrec(-1, 3)), '-0.001')
    self.assertEqual(str(FixedPrec(-1003, 3)), '-1.003')
