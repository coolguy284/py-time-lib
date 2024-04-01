import unittest

from ..calendars.gregorian import GregorianDate
from ..fixed_prec import FixedPrec
from ..time_classes import TimeDelta, TimeInstant

class TestTimeClasses(unittest.TestCase):
  def __init__(self, *args):
    super().__init__(*args)
    self.maxDiff = None
  
  def test_time_delta_str(self):
    self.assertEqual(str(TimeDelta(FixedPrec(1000, 0))), 'TD+1000')
    self.assertEqual(str(TimeDelta(FixedPrec(-1000, 0))), 'TD-1000')
    self.assertEqual(str(TimeDelta(FixedPrec(0, 0))), 'TD+0')
  
  def test_time_instant_str(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0))), 'T+1000')
    self.assertEqual(str(TimeInstant(FixedPrec(-1000, 0))), 'T-1000')
    self.assertEqual(str(TimeInstant(FixedPrec(0, 0))), 'T+0')
  
  def test_time_delta_basic_ops(self):
    self.assertEqual(str(-TimeDelta(FixedPrec(1, 0))), 'TD-1')
    self.assertEqual(str(-TimeDelta(FixedPrec(0, 0))), 'TD+0')
    self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) + TimeDelta(FixedPrec(2, 0))), 'TD+5')
    self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) - TimeDelta(FixedPrec(2, 0))), 'TD+1')
    self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) * FixedPrec(4, 0)), 'TD+12')
    #self.assertEqual(str(TimeDelta(FixedPrec(3, 0)) / FixedPrec(3, 0)), 'TD+1')
  
  def test_time_instant_basic_ops(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0)) + TimeDelta(FixedPrec(3, 0))), 'T+1003')
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0)) - TimeDelta(FixedPrec(3, 0))), 'T+997')
    self.assertEqual(str(TimeInstant(FixedPrec(1000, 0)) - TimeInstant(FixedPrec(993, 0))), 'TD+7')
  
  def test_time_delta_relational_ops(self):
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) > TimeDelta(FixedPrec(0, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) < TimeDelta(FixedPrec(0, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) >= TimeDelta(FixedPrec(0, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) <= TimeDelta(FixedPrec(0, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) == TimeDelta(FixedPrec(0, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) != TimeDelta(FixedPrec(0, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) > TimeDelta(FixedPrec(1, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) < TimeDelta(FixedPrec(1, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) >= TimeDelta(FixedPrec(1, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) <= TimeDelta(FixedPrec(1, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) == TimeDelta(FixedPrec(1, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) != TimeDelta(FixedPrec(1, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) > TimeDelta(FixedPrec(2, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) < TimeDelta(FixedPrec(2, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) >= TimeDelta(FixedPrec(2, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) <= TimeDelta(FixedPrec(2, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) == TimeDelta(FixedPrec(2, 0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) != TimeDelta(FixedPrec(2, 0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) == None, False)
    self.assertEqual(TimeDelta(FixedPrec(1, 0)) != None, True)
  
  def test_time_instant_relational_ops(self):
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) > TimeInstant(FixedPrec(0, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) < TimeInstant(FixedPrec(0, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) >= TimeInstant(FixedPrec(0, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) <= TimeInstant(FixedPrec(0, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) == TimeInstant(FixedPrec(0, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) != TimeInstant(FixedPrec(0, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) > TimeInstant(FixedPrec(1, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) < TimeInstant(FixedPrec(1, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) >= TimeInstant(FixedPrec(1, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) <= TimeInstant(FixedPrec(1, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) == TimeInstant(FixedPrec(1, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) != TimeInstant(FixedPrec(1, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) > TimeInstant(FixedPrec(2, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) < TimeInstant(FixedPrec(2, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) >= TimeInstant(FixedPrec(2, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) <= TimeInstant(FixedPrec(2, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) == TimeInstant(FixedPrec(2, 0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) != TimeInstant(FixedPrec(2, 0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) == None, False)
    self.assertEqual(TimeInstant(FixedPrec(1, 0)) != None, True)
  
  def test_time_type_coercion(self):
    self.assertEqual(TimeDelta(3), TimeDelta(FixedPrec(3, 0)))
    self.assertEqual(TimeDelta(3.0), TimeDelta(FixedPrec(3, 0)))
    self.assertEqual(TimeInstant(3), TimeInstant(FixedPrec(3, 0)))
    self.assertEqual(TimeInstant(3.0), TimeInstant(FixedPrec(3, 0)))
  
  def test_utc_conversion_positive_leap_sec(self):
    last_leap_index = 53
    second_last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 3][0]
    last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1][0]
    second_last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2][2]
    last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index][2]
    last_leap_utc_secs = last_leap_start + last_utc_offset + 1
    second_last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2][3]
    last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1][3]
    self.assertEqual(last_leap_utc_secs, GregorianDate(2017, 1, 1).to_days_since_epoch() * 86400)
    self.assertEqual(second_last_utc_offset, -36)
    self.assertEqual(last_utc_offset, -37)
    t1 = TimeInstant(last_leap_start)
    t0 = t1 - TimeDelta('0.1')
    t2 = t1 + TimeDelta('0.1')
    t3 = t1 + TimeDelta('0.9')
    t4 = t1 + TimeDelta('1.0')
    t5 = t1 + TimeDelta('1.1')
    t6 = t1 + TimeDelta('1.9')
    t7 = t1 + TimeDelta('2.0')
    t8 = t1 + TimeDelta('2.1')
    self.assertEqual(t0.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs - FixedPrec('0.1'),
      'positive_leap_second_occurring': False,
      'last_leap_delta': second_last_leap_delta,
      'last_leap_transition_time': second_last_leap_start + 1,
    })
    self.assertEqual(t0.to_utc_secs_since_epoch(), (
      last_leap_utc_secs - FixedPrec('0.1'),
      False,
    ))
    self.assertEqual(t1.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs,
      'positive_leap_second_occurring': True,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start,
    })
    self.assertEqual(t1.to_utc_secs_since_epoch(), (
      last_leap_utc_secs,
      False,
    ))
    self.assertEqual(t2.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs,
      'positive_leap_second_occurring': True,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start,
    })
    self.assertEqual(t2.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('0.1'),
      False,
    ))
    self.assertEqual(t3.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs,
      'positive_leap_second_occurring': True,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start,
    })
    self.assertEqual(t3.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('0.9'),
      False,
    ))
    self.assertEqual(t4.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs,
      'positive_leap_second_occurring': False,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start + 1,
    })
    self.assertEqual(t4.to_utc_secs_since_epoch(), (
      last_leap_utc_secs,
      True,
    ))
    self.assertEqual(t5.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('0.1'),
      'positive_leap_second_occurring': False,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start + 1,
    })
    self.assertEqual(t5.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('0.1'),
      True,
    ))
    self.assertEqual(t6.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('0.9'),
      'positive_leap_second_occurring': False,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start + 1,
    })
    self.assertEqual(t6.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('0.9'),
      True,
    ))
    self.assertEqual(t7.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('1.0'),
      'positive_leap_second_occurring': False,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start + 1,
    })
    self.assertEqual(t7.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('1.0'),
      False,
    ))
    self.assertEqual(t8.to_utc_info(), {
      'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('1.1'),
      'positive_leap_second_occurring': False,
      'last_leap_delta': last_leap_delta,
      'last_leap_transition_time': last_leap_start + 1,
    })
    self.assertEqual(t8.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('1.1'),
      False,
    ))
  
  def test_utc_conversion_negative_leap_sec(self):
    with TimeInstant._temp_add_leap_sec(27, ('2017-12-31', FixedPrec(1, 0))):
      #print('\n'.join([repr(i) for i in TimeInstant.TAI_TO_UTC_OFFSET_TABLE]))
      last_leap_index = 54
      second_last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2][0]
      last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index][0]
      second_last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1][2]
      last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index][2]
      last_leap_utc_secs = last_leap_start + last_utc_offset - 1
      second_last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1][3]
      last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index][3]
      self.assertEqual(last_leap_utc_secs, GregorianDate(2018, 1, 1).to_days_since_epoch() * 86400 - 1)
      self.assertEqual(second_last_utc_offset, -37)
      self.assertEqual(last_utc_offset, -36)
      t1 = TimeInstant(last_leap_start)
      t0 = t1 - TimeDelta('0.1')
      t2 = t1 + TimeDelta('0.1')
      t3 = t1 + TimeDelta('0.9')
      t4 = t1 + TimeDelta('1.0')
      t5 = t1 + TimeDelta('1.1')
      self.assertEqual(t0.to_utc_info(), {
        'utc_seconds_since_epoch': last_leap_utc_secs - FixedPrec('0.1'),
        'positive_leap_second_occurring': False,
        'last_leap_delta': second_last_leap_delta,
        'last_leap_transition_time': second_last_leap_start + 1,
      })
      self.assertEqual(t0.to_utc_secs_since_epoch(), (
        last_leap_utc_secs - FixedPrec('0.1'),
        False,
      ))
      self.assertEqual(t1.to_utc_info(), {
        'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('1.0'),
        'positive_leap_second_occurring': False,
        'last_leap_delta': last_leap_delta,
        'last_leap_transition_time': last_leap_start,
      })
      self.assertEqual(t1.to_utc_secs_since_epoch(), (
        last_leap_utc_secs + FixedPrec('1.0'),
        False,
      ))
      self.assertEqual(t2.to_utc_info(), {
        'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('1.1'),
        'positive_leap_second_occurring': False,
        'last_leap_delta': last_leap_delta,
        'last_leap_transition_time': last_leap_start,
      })
      self.assertEqual(t2.to_utc_secs_since_epoch(), (
        last_leap_utc_secs + FixedPrec('1.1'),
        False,
      ))
      self.assertEqual(t3.to_utc_info(), {
        'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('1.9'),
        'positive_leap_second_occurring': False,
        'last_leap_delta': last_leap_delta,
        'last_leap_transition_time': last_leap_start,
      })
      self.assertEqual(t3.to_utc_secs_since_epoch(), (
        last_leap_utc_secs + FixedPrec('1.9'),
        False,
      ))
      self.assertEqual(t4.to_utc_info(), {
        'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('2.0'),
        'positive_leap_second_occurring': False,
        'last_leap_delta': last_leap_delta,
        'last_leap_transition_time': last_leap_start,
      })
      self.assertEqual(t4.to_utc_secs_since_epoch(), (
        last_leap_utc_secs + FixedPrec('2.0'),
        False,
      ))
      self.assertEqual(t5.to_utc_info(), {
        'utc_seconds_since_epoch': last_leap_utc_secs + FixedPrec('2.1'),
        'positive_leap_second_occurring': False,
        'last_leap_delta': last_leap_delta,
        'last_leap_transition_time': last_leap_start,
      })
      self.assertEqual(t5.to_utc_secs_since_epoch(), (
        last_leap_utc_secs + FixedPrec('2.1'),
        False,
      ))
  
  def test_tai_tuple(self):
    date = GregorianDate(2018, 1, 1)
    instant = TimeInstant(date.to_days_since_epoch() * 86400 + 37.5)
    self.assertEqual(instant.to_gregorian_date_tuple_tai(), (2018, 1, 1, 0, 0, 37, 0.5))
  
  def test_utc_tuple(self):
    date = GregorianDate(2018, 1, 1)
    instant = TimeInstant(date.to_days_since_epoch() * 86400 + 37.5)
    self.assertEqual(instant.to_gregorian_date_tuple_utc(), (2018, 1, 1, 0, 0, 0, 0.5))
