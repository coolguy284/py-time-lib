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
  
  def test_utc_conversion_basic(self):
    last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[-2][0]
    last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[-1][2]
    self.assertEqual(last_utc_offset, -37)
    t1 = TimeInstant(last_leap_start)
    t0 = t1 - TimeDelta(0.1)
    t2 = t1 + TimeDelta(0.1)
    t3 = t1 + TimeDelta(0.9)
    t4 = t1 + TimeDelta(1.0)
    t5 = t1 + TimeDelta(1.1)
    t6 = t1 + TimeDelta(1.9)
    t7 = t1 + TimeDelta(2.0)
    t8 = t1 + TimeDelta(2.1)
    self.assertEqual(t0.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_start + last_utc_offset + 1 - FixedPrec.from_basic(0.1),
      'positive_leap_second_occurring': False,
      'last_leap_delta': TimeInstant.TAI_TO_UTC_OFFSET_TABLE[-3][3],
      'time_since_last_leap_second_start': last_leap_start - TimeInstant.TAI_TO_UTC_OFFSET_TABLE[-3][0] - 0.1,
    })
