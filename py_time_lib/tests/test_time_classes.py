import unittest

from ..fixed_prec import FixedPrec
from ..time_classes import TimeDelta, TimeInstant

class TestTimeClasses(unittest.TestCase):
  def test_time_delta_str(self):
    self.assertEqual(str(TimeDelta(FixedPrec(1000, 0))), 'TD+1000')
    self.assertEqual(str(TimeDelta(FixedPrec(-1000, 0))), 'TD-1000')
    self.assertEqual(str(TimeDelta(FixedPrec(0, 0))), 'TD+0')
  
  def test_time_instant_str(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0))), 'T+1000')
    self.assertEqual(str(TimeInstant(FixedPrec(-1000, 0))), 'T-1000')
    self.assertEqual(str(TimeInstant(FixedPrec(0, 0))), 'T+0')
  
  def test_time_delta_ops(self):
    self.assertEqual(str(-TimeDelta(FixedPrec(1, 0))), 'TD-1')
    self.assertEqual(str(-TimeDelta(FixedPrec(0, 0))), 'TD+0')
    self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) + TimeDelta(FixedPrec(2, 0))), 'TD+5')
    self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) - TimeDelta(FixedPrec(2, 0))), 'TD+1')
    self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) * FixedPrec(4, 0)), 'TD+12')
    #self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) / FixedPrec(3, 0)), 'TD+1')
  
  def test_time_instant_add_sub(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0)) + TimeDelta(FixedPrec(3, 0))), 'T+1003')
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0)) - TimeDelta(FixedPrec(3, 0))), 'T+997')
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0)) - TimeInstant(FixedPrec(993, 0))), 'TD+7')
