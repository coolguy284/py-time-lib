from time import time_ns
import datetime
import unittest

from .. import FixedPrec, GregorianDate, TimeDelta, TimeInstant
from ..data.leap_seconds import NOMINAL_SECS_PER_DAY

class TestTimeClasses(unittest.TestCase):
  def __init__(self, *args):
    super().__init__(*args)
    self.maxDiff = None
  
  def test_time_delta_str(self):
    self.assertEqual(str(TimeDelta(FixedPrec(1000))), 'TD+1000')
    self.assertEqual(str(TimeDelta(FixedPrec(-1000))), 'TD-1000')
    self.assertEqual(str(TimeDelta(FixedPrec(0))), 'TD+0')
  
  def test_time_instant_str(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000))), 'T+1000')
    self.assertEqual(str(TimeInstant(FixedPrec(-1000))), 'T-1000')
    self.assertEqual(str(TimeInstant(FixedPrec(0))), 'T+0')
  
  def test_time_delta_repr(self):
    self.assertEqual(repr(TimeDelta(FixedPrec(1000))), 'TimeDelta(FixedPrec(value = 1000, place = 0, max_prec = 12))')
    self.assertEqual(repr(TimeDelta(FixedPrec(-1000))), 'TimeDelta(FixedPrec(value = -1000, place = 0, max_prec = 12))')
    self.assertEqual(repr(TimeDelta(FixedPrec(0))), 'TimeDelta(FixedPrec(value = 0, place = 0, max_prec = 12))')
  
  def test_time_instant_repr(self):
    self.assertEqual(repr(TimeInstant(FixedPrec(1000))), 'TimeInstant(FixedPrec(value = 1000, place = 0, max_prec = 12))')
    self.assertEqual(repr(TimeInstant(FixedPrec(-1000))), 'TimeInstant(FixedPrec(value = -1000, place = 0, max_prec = 12))')
    self.assertEqual(repr(TimeInstant(FixedPrec(0))), 'TimeInstant(FixedPrec(value = 0, place = 0, max_prec = 12))')
  
  def test_time_delta_basic_ops(self):
    self.assertEqual(str(-TimeDelta(FixedPrec(1))), 'TD-1')
    self.assertEqual(str(-TimeDelta(FixedPrec(0))), 'TD+0')
    self.assertEqual(str(+TimeDelta(FixedPrec(1))), 'TD+1')
    self.assertEqual(str(+TimeDelta(FixedPrec(0))), 'TD+0')
    self.assertEqual(str(abs(TimeDelta(FixedPrec(1)))), 'TD+1')
    self.assertEqual(str(abs(TimeDelta(FixedPrec(0)))), 'TD+0')
    self.assertEqual(str(abs(TimeDelta(FixedPrec(-1)))), 'TD+1')
    self.assertEqual(str(TimeDelta(FixedPrec(3)) + TimeDelta(FixedPrec(2))), 'TD+5')
    self.assertEqual(str(TimeDelta(FixedPrec(3)) - TimeDelta(FixedPrec(2))), 'TD+1')
    self.assertEqual(str(TimeDelta(FixedPrec(3)) * FixedPrec(4)), 'TD+12')
    self.assertEqual(TimeDelta(FixedPrec(3)) / FixedPrec(3), TimeDelta(FixedPrec(1)))
  
  def test_time_instant_basic_ops(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) + TimeDelta(FixedPrec(3))), 'T+1003')
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) - TimeDelta(FixedPrec(3))), 'T+997')
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) - TimeInstant(FixedPrec(993))), 'TD+7')
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) + TimeDelta(FixedPrec('0.1'))), 'T+1000.1')
  
  def test_time_delta_relational_ops(self):
    self.assertEqual(TimeDelta(FixedPrec(1)) > TimeDelta(FixedPrec(0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) < TimeDelta(FixedPrec(0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) >= TimeDelta(FixedPrec(0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) <= TimeDelta(FixedPrec(0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) == TimeDelta(FixedPrec(0)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) != TimeDelta(FixedPrec(0)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) > TimeDelta(FixedPrec(1)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) < TimeDelta(FixedPrec(1)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) >= TimeDelta(FixedPrec(1)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) <= TimeDelta(FixedPrec(1)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) == TimeDelta(FixedPrec(1)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) != TimeDelta(FixedPrec(1)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) > TimeDelta(FixedPrec(2)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) < TimeDelta(FixedPrec(2)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) >= TimeDelta(FixedPrec(2)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) <= TimeDelta(FixedPrec(2)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) == TimeDelta(FixedPrec(2)), False)
    self.assertEqual(TimeDelta(FixedPrec(1)) != TimeDelta(FixedPrec(2)), True)
    self.assertEqual(TimeDelta(FixedPrec(1)) == None, False)
    self.assertEqual(TimeDelta(FixedPrec(1)) != None, True)
  
  def test_time_instant_relational_ops(self):
    self.assertEqual(TimeInstant(FixedPrec(1)) > TimeInstant(FixedPrec(0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) < TimeInstant(FixedPrec(0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) >= TimeInstant(FixedPrec(0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) <= TimeInstant(FixedPrec(0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) == TimeInstant(FixedPrec(0)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) != TimeInstant(FixedPrec(0)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) > TimeInstant(FixedPrec(1)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) < TimeInstant(FixedPrec(1)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) >= TimeInstant(FixedPrec(1)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) <= TimeInstant(FixedPrec(1)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) == TimeInstant(FixedPrec(1)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) != TimeInstant(FixedPrec(1)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) > TimeInstant(FixedPrec(2)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) < TimeInstant(FixedPrec(2)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) >= TimeInstant(FixedPrec(2)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) <= TimeInstant(FixedPrec(2)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) == TimeInstant(FixedPrec(2)), False)
    self.assertEqual(TimeInstant(FixedPrec(1)) != TimeInstant(FixedPrec(2)), True)
    self.assertEqual(TimeInstant(FixedPrec(1)) == None, False)
    self.assertEqual(TimeInstant(FixedPrec(1)) != None, True)
  
  def test_time_type_coercion(self):
    self.assertEqual(TimeDelta(3), TimeDelta(FixedPrec(3)))
    self.assertEqual(TimeDelta(3.0), TimeDelta(FixedPrec(3)))
    self.assertEqual(TimeInstant(3), TimeInstant(FixedPrec(3)))
    self.assertEqual(TimeInstant(3.0), TimeInstant(FixedPrec(3)))
  
  def test_utc_conversion_positive_leap_sec(self):
    last_leap_index = 53
    second_last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 3]['start_instant']
    last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['start_instant']
    second_last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2]['utc_tai_delta']
    last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index]['utc_tai_delta']
    last_leap_utc_secs = last_leap_start + last_utc_offset + 1
    second_last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2]['leap_utc_delta']
    last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['leap_utc_delta']
    self.assertEqual(last_leap_utc_secs, GregorianDate(2017, 1, 1).days_since_epoch * 86400)
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
      'current_utc_tai_offset': -36,
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
      'current_utc_tai_offset': -36,
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
      'current_utc_tai_offset': -36,
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
      'current_utc_tai_offset': -36,
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
      'current_utc_tai_offset': -37,
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
      'current_utc_tai_offset': -37,
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
      'current_utc_tai_offset': -37,
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
      'current_utc_tai_offset': -37,
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
      'current_utc_tai_offset': -37,
    })
    self.assertEqual(t8.to_utc_secs_since_epoch(), (
      last_leap_utc_secs + FixedPrec('1.1'),
      False,
    ))
  
  def test_utc_conversion_negative_leap_sec(self):
    with TimeInstant._temp_add_leap_sec(27, ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1))):
      #print('\n'.join([repr((i, GregorianDate.from_days_since_epoch(round(int(i['start_instant']) / 86400)))) for i in TimeInstant.TAI_TO_UTC_OFFSET_TABLE]))
      last_leap_index = 54
      second_last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2]['start_instant']
      last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index]['start_instant']
      second_last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['utc_tai_delta']
      last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index]['utc_tai_delta']
      last_leap_utc_secs = last_leap_start + last_utc_offset - 1
      second_last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['leap_utc_delta']
      last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index]['leap_utc_delta']
      self.assertEqual(last_leap_utc_secs, GregorianDate(2018, 1, 1).days_since_epoch * 86400 - 1)
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
        'current_utc_tai_offset': -37,
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
        'current_utc_tai_offset': -36,
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
        'current_utc_tai_offset': -36,
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
        'current_utc_tai_offset': -36,
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
        'current_utc_tai_offset': -36,
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
        'current_utc_tai_offset': -36,
      })
      self.assertEqual(t5.to_utc_secs_since_epoch(), (
        last_leap_utc_secs + FixedPrec('2.1'),
        False,
      ))
  
  def test_tai_tuple(self):
    date = GregorianDate(2018, 1, 1)
    instant = TimeInstant(date.days_since_epoch * 86400 + 37.5)
    self.assertEqual(instant.to_date_tuple_tai(), (2018, 1, 1, 0, 0, 37, 0.5))
  
  def test_utc_tuple(self):
    date = GregorianDate(2018, 1, 1)
    instant = TimeInstant(date.days_since_epoch * 86400 + 37.5)
    self.assertEqual(instant.to_date_tuple_utc(), (2018, 1, 1, 0, 0, 0, 0.5))
  
  def test_from_utc(self):
    def test_one(time):
      instant = TimeInstant(time)
      self.assertEqual(instant, TimeInstant.from_utc_secs_since_epoch(*instant.to_utc_secs_since_epoch()))
    
    with TimeInstant._temp_add_leap_sec(27, ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1))):
      pos_leap_sec_start = 52
      neg_leap_sec = 54
      
      test_one(0)
      
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] - FixedPrec('0.1'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'])
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('0.1'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('0.9'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('1.0'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('1.1'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('1.9'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('2.0'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[pos_leap_sec_start]['start_instant'] + FixedPrec('2.1'))
      
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'] - FixedPrec('0.1'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'])
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'] + FixedPrec('0.1'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'] + FixedPrec('0.9'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'] + FixedPrec('1.0'))
      test_one(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'] + FixedPrec('1.1'))
      
      instant_before_neg_leap = TimeInstant(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[neg_leap_sec]['start_instant'] - FixedPrec('0.1'))
      utc_before_neg_leap = instant_before_neg_leap.to_utc_secs_since_epoch()[0]
      
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap, round_invalid_time_upwards = True),
        instant_before_neg_leap
      )
      #print('\n'.join([repr(i) for i in TimeInstant.UTC_TO_TAI_OFFSET_TABLE]))
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('0.1'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('0.2'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('1.0'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('1.1'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('1.2'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.2'))
      )
      
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap, round_invalid_time_upwards = False),
        instant_before_neg_leap
      )
      
      with self.assertRaises(Exception):
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('0.1'), round_invalid_time_upwards = False)
      
      with self.assertRaises(Exception):
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('0.2'), round_invalid_time_upwards = False)
      
      with self.assertRaises(Exception):
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('1.0'), round_invalid_time_upwards = False)
      
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('1.1'), round_invalid_time_upwards = False),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_utc_secs_since_epoch(utc_before_neg_leap + FixedPrec('1.2'), round_invalid_time_upwards = False),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.2'))
      )
  
  def test_tai_utc_tuple_leap_secs(self):
    with TimeInstant._temp_add_leap_secs(27, [
        ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1)),
        ('2018-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-2)),
        ('2018-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(2)),
      ]):
      
      leap_normal_pos_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2017, 1, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_normal_neg_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2018, 1, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_big_pos_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2018, 7, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_big_neg_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2019, 1, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      
      def test_instant(time_delta, tai_tuple, utc_tuple):
        instant = current_leap + TimeDelta(FixedPrec(time_delta))
        self.assertEqual(instant.to_date_tuple_tai(), tai_tuple[:6] + (FixedPrec(tai_tuple[6]),))
        self.assertEqual(instant.to_date_tuple_utc(), utc_tuple[:6] + (FixedPrec(utc_tuple[6]),))
      
      # positive leap second (36 -> 37)
      
      current_leap = leap_normal_pos_midnight
      
      test_instant('-0.1', (2017, 1, 1, 0, 0, 35, '0.9'), (2016, 12, 31, 23, 59, 59, '0.9'))
      test_instant('0',    (2017, 1, 1, 0, 0, 36, '0'  ), (2016, 12, 31, 23, 59, 60, '0'  ))
      test_instant('0.1',  (2017, 1, 1, 0, 0, 36, '0.1'), (2016, 12, 31, 23, 59, 60, '0.1'))
      test_instant('0.9',  (2017, 1, 1, 0, 0, 36, '0.9'), (2016, 12, 31, 23, 59, 60, '0.9'))
      test_instant('1',    (2017, 1, 1, 0, 0, 37, '0'  ), (2017, 1,  1,  0,  0,  0,  '0'  ))
      test_instant('1.1',  (2017, 1, 1, 0, 0, 37, '0.1'), (2017, 1,  1,  0,  0,  0,  '0.1'))
      test_instant('1.9',  (2017, 1, 1, 0, 0, 37, '0.9'), (2017, 1,  1,  0,  0,  0,  '0.9'))
      test_instant('2',    (2017, 1, 1, 0, 0, 38, '0'  ), (2017, 1,  1,  0,  0,  1,  '0'  ))
      test_instant('2.1',  (2017, 1, 1, 0, 0, 38, '0.1'), (2017, 1,  1,  0,  0,  1,  '0.1'))
      
      # negative leap second (37 -> 36)
      
      current_leap = leap_normal_neg_midnight
      
      test_instant('-0.1', (2018, 1, 1, 0, 0, 35, '0.9'), (2017, 12, 31, 23, 59, 58, '0.9'))
      test_instant('0',    (2018, 1, 1, 0, 0, 36, '0'  ), (2018, 1,  1,  0,  0,  0,  '0'  ))
      test_instant('0.1',  (2018, 1, 1, 0, 0, 36, '0.1'), (2018, 1,  1,  0,  0,  0,  '0.1'))
      test_instant('0.9',  (2018, 1, 1, 0, 0, 36, '0.9'), (2018, 1,  1,  0,  0,  0,  '0.9'))
      test_instant('1',    (2018, 1, 1, 0, 0, 37, '0'  ), (2018, 1,  1,  0,  0,  1,  '0'  ))
      test_instant('1.1',  (2018, 1, 1, 0, 0, 37, '0.1'), (2018, 1,  1,  0,  0,  1,  '0.1'))
      
      # doubly positive leap second (36 -> 38)
      
      current_leap = leap_big_pos_midnight
      
      test_instant('-0.1', (2018, 7, 1, 0, 0, 35, '0.9'), (2018, 6, 30, 23, 59, 59, '0.9'))
      test_instant('0',    (2018, 7, 1, 0, 0, 36, '0'  ), (2018, 6, 30, 23, 59, 60, '0'  ))
      test_instant('0.1',  (2018, 7, 1, 0, 0, 36, '0.1'), (2018, 6, 30, 23, 59, 60, '0.1'))
      test_instant('0.9',  (2018, 7, 1, 0, 0, 36, '0.9'), (2018, 6, 30, 23, 59, 60, '0.9'))
      test_instant('1',    (2018, 7, 1, 0, 0, 37, '0'  ), (2018, 6, 30, 23, 59, 61, '0'  ))
      test_instant('1.1',  (2018, 7, 1, 0, 0, 37, '0.1'), (2018, 6, 30, 23, 59, 61, '0.1'))
      test_instant('1.9',  (2018, 7, 1, 0, 0, 37, '0.9'), (2018, 6, 30, 23, 59, 61, '0.9'))
      test_instant('2',    (2018, 7, 1, 0, 0, 38, '0'  ), (2018, 7,  1,  0,  0,  0, '0'  ))
      test_instant('2.1',  (2018, 7, 1, 0, 0, 38, '0.1'), (2018, 7,  1,  0,  0,  0, '0.1'))
      test_instant('2.9',  (2018, 7, 1, 0, 0, 38, '0.9'), (2018, 7,  1,  0,  0,  0, '0.9'))
      test_instant('3',    (2018, 7, 1, 0, 0, 39, '0'  ), (2018, 7,  1,  0,  0,  1, '0'  ))
      test_instant('3.1',  (2018, 7, 1, 0, 0, 39, '0.1'), (2018, 7,  1,  0,  0,  1, '0.1'))
      test_instant('3.9',  (2018, 7, 1, 0, 0, 39, '0.9'), (2018, 7,  1,  0,  0,  1, '0.9'))
      test_instant('4',    (2018, 7, 1, 0, 0, 40, '0'  ), (2018, 7,  1,  0,  0,  2, '0'  ))
      test_instant('4.1',  (2018, 7, 1, 0, 0, 40, '0.1'), (2018, 7,  1,  0,  0,  2, '0.1'))
      
      # doubly negative leap second (38 -> 36)
      
      current_leap = leap_big_neg_midnight
      
      test_instant('-0.1', (2019, 1, 1, 0, 0, 35, '0.9'), (2018, 12, 31, 23, 59, 57, '0.9'))
      test_instant('0',    (2019, 1, 1, 0, 0, 36, '0'  ), (2019, 1,  1,  0,  0,  0,  '0'  ))
      test_instant('0.1',  (2019, 1, 1, 0, 0, 36, '0.1'), (2019, 1,  1,  0,  0,  0,  '0.1'))
      test_instant('0.9',  (2019, 1, 1, 0, 0, 36, '0.9'), (2019, 1,  1,  0,  0,  0,  '0.9'))
      test_instant('1',    (2019, 1, 1, 0, 0, 37, '0'  ), (2019, 1,  1,  0,  0,  1,  '0'  ))
      test_instant('1.1',  (2019, 1, 1, 0, 0, 37, '0.1'), (2019, 1,  1,  0,  0,  1,  '0.1'))
      test_instant('1.9',  (2019, 1, 1, 0, 0, 37, '0.9'), (2019, 1,  1,  0,  0,  1,  '0.9'))
      test_instant('2',    (2019, 1, 1, 0, 0, 38, '0'  ), (2019, 1,  1,  0,  0,  2,  '0'  ))
      test_instant('2.1',  (2019, 1, 1, 0, 0, 38, '0.1'), (2019, 1,  1,  0,  0,  2,  '0.1'))
  
  def test_from_tai_tuple(self):
    tai_tuple = 2018, 1, 1, 3, 2, 9, FixedPrec('0.1')
    self.assertEqual(TimeInstant.from_date_tuple_tai(*tai_tuple).to_date_tuple_tai(), tai_tuple)
  
  def test_from_utc_tuple(self):
    with TimeInstant._temp_add_leap_secs(27, [
        ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1)),
        ('2018-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-2)),
        ('2018-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(2)),
      ]):
      
      def test(*date_tuple):
        date_tuple = *date_tuple[:6], FixedPrec(date_tuple[6])
        instant = TimeInstant.from_date_tuple_utc(*date_tuple)
        self.assertEqual(date_tuple, instant.to_date_tuple_utc())
      
      test(2016, 12, 31, 23, 59, 59, '0.9')
      test(2016, 12, 31, 23, 59, 60, '0'  )
      test(2016, 12, 31, 23, 59, 60, '0.1')
      test(2016, 12, 31, 23, 59, 60, '0.9')
      test(2017, 1,  1,  0,  0,  0,  '0'  )
      test(2017, 1,  1,  0,  0,  0,  '0.1')
      test(2017, 1,  1,  0,  0,  0,  '0.9')
      test(2017, 1,  1,  0,  0,  1,  '0'  )
      test(2017, 1,  1,  0,  0,  1,  '0.1')
      
      test(2017, 12, 31, 23, 59, 58, '0.9')
      test(2018, 1,  1,  0,  0,  0,  '0'  )
      test(2018, 1,  1,  0,  0,  0,  '0.1')
      test(2018, 1,  1,  0,  0,  0,  '0.9')
      test(2018, 1,  1,  0,  0,  1,  '0'  )
      test(2018, 1,  1,  0,  0,  1,  '0.1')
      
      test(2018, 6, 30, 23, 59, 59, '0.9')
      test(2018, 6, 30, 23, 59, 60, '0'  )
      test(2018, 6, 30, 23, 59, 60, '0.1')
      test(2018, 6, 30, 23, 59, 60, '0.9')
      test(2018, 6, 30, 23, 59, 61, '0'  )
      test(2018, 6, 30, 23, 59, 61, '0.1')
      test(2018, 6, 30, 23, 59, 61, '0.9')
      test(2018, 7,  1,  0,  0,  0, '0'  )
      test(2018, 7,  1,  0,  0,  0, '0.1')
      test(2018, 7,  1,  0,  0,  0, '0.9')
      test(2018, 7,  1,  0,  0,  1, '0'  )
      test(2018, 7,  1,  0,  0,  1, '0.1')
      test(2018, 7,  1,  0,  0,  1, '0.9')
      test(2018, 7,  1,  0,  0,  2, '0'  )
      test(2018, 7,  1,  0,  0,  2, '0.1')
      
      test(2018, 12, 31, 23, 59, 57, '0.9')
      test(2019, 1,  1,  0,  0,  0,  '0'  )
      test(2019, 1,  1,  0,  0,  0,  '0.1')
      test(2019, 1,  1,  0,  0,  0,  '0.9')
      test(2019, 1,  1,  0,  0,  1,  '0'  )
      test(2019, 1,  1,  0,  0,  1,  '0.1')
      test(2019, 1,  1,  0,  0,  1,  '0.9')
      test(2019, 1,  1,  0,  0,  2,  '0'  )
      test(2019, 1,  1,  0,  0,  2,  '0.1')
  
  def test_to_unix_timestamp(self):
    self.assertEqual(TimeInstant.from_date_tuple_utc(1970, 1, 1, 0, 0, 0, 0).to_unix_timestamp(), (0, False))
  
  def test_from_unix_timestamp(self):
    self.assertEqual(TimeInstant.from_unix_timestamp(0).to_date_tuple_utc(), (1970, 1, 1, 0, 0, 0, 0))
  
  def test_jd(self):
    # https://aa.usno.navy.mil/calculated/juliandate?ID=AA&date=2024-04-09&era=AD&time=20%3A30%3A55.000&submit=Get+Date
    past_date_tuple = 2024, 4, 9, 20, 30, 54, 0
    date_tuple = 2024, 4, 9, 20, 30, 55, 0
    instant = TimeInstant.from_date_tuple_tai(*date_tuple)
    self.assertTrue(
      abs(instant.to_julian_date_tai() - FixedPrec('2460410.354803')) < FixedPrec('0.000001'),
      f'{instant.to_julian_date_tai()} {FixedPrec('2460410.354803')}'
    )
    self.assertTrue(
      abs(instant.to_reduced_julian_date_tai() - FixedPrec('60410.354803')) < FixedPrec('0.000001'),
      f'{instant.to_reduced_julian_date_tai()} {FixedPrec('60410.354803')}'
    )
    self.assertTrue(
      abs(instant.to_modified_julian_date_tai() - FixedPrec('60409.854803')) < FixedPrec('0.000001'),
      f'{instant.to_modified_julian_date_tai()} {FixedPrec('60409.854803')}'
    )
    from_jd = TimeInstant.from_julian_date_tai(instant.to_julian_date_tai()).to_date_tuple_tai()
    self.assertTrue(from_jd[:6] == date_tuple[:6] or from_jd[:6] == past_date_tuple[:6])
    from_jd = TimeInstant.from_reduced_julian_date_tai(instant.to_reduced_julian_date_tai()).to_date_tuple_tai()
    self.assertTrue(from_jd[:6] == date_tuple[:6] or from_jd[:6] == past_date_tuple[:6])
    from_jd = TimeInstant.from_modified_julian_date_tai(instant.to_modified_julian_date_tai()).to_date_tuple_tai()
    self.assertTrue(from_jd[:6] == date_tuple[:6] or from_jd[:6] == past_date_tuple[:6])
  
  def test_days_and_secs_to_mins_since_epoch(self):
    self.assertEqual(TimeInstant.days_and_secs_to_mins_since_epoch(2, FixedPrec('120.3')), (2 * 1440 + 2, FixedPrec('0.3')))
    self.assertEqual(TimeInstant.mins_to_days_and_secs_since_epoch(2 * 1440 + 2, FixedPrec('0.3')), (2, FixedPrec('120.3')))
    
    self.assertEqual(TimeInstant.days_and_secs_to_mins_since_epoch(-2, FixedPrec('120.3')), (-2 * 1440 + 2, FixedPrec('0.3')))
    self.assertEqual(TimeInstant.mins_to_days_and_secs_since_epoch(-2 * 1440 + 2, FixedPrec('0.3')), (-2, FixedPrec('120.3')))
    
    self.assertEqual(TimeInstant.days_and_secs_to_mins_since_epoch(0, FixedPrec('120.3')), (2, FixedPrec('0.3')))
    self.assertEqual(TimeInstant.mins_to_days_and_secs_since_epoch(2, FixedPrec('0.3')), (0, FixedPrec('120.3')))
  
  def test_days_h_m_to_mins_since_epoch(self):
    self.assertEqual(TimeInstant.days_h_m_to_mins_since_epoch(2, 3, 4), 2 * 1440 + 3 * 60 + 4)
    self.assertEqual(TimeInstant.mins_since_epoch_to_days_h_m(2 * 1440 + 3 * 60 + 4), (2, 3, 4))
    
    self.assertEqual(TimeInstant.days_h_m_to_mins_since_epoch(-2, 3, 4), -2 * 1440 + 3 * 60 + 4)
    self.assertEqual(TimeInstant.mins_since_epoch_to_days_h_m(-2 * 1440 + 3 * 60 + 4), (-2, 3, 4))
    
    self.assertEqual(TimeInstant.days_h_m_to_mins_since_epoch(0, 3, 4), 3 * 60 + 4)
    self.assertEqual(TimeInstant.mins_since_epoch_to_days_h_m(3 * 60 + 4), (0, 3, 4))
  
  def test_get_utc_tai_offset(self):
    first_leap_index = 0
    last_leap_index = 53
    
    t1 = TimeInstant(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[first_leap_index]['start_instant'])
    t0 = t1 - TimeDelta('0.1')
    t2 = t1 + TimeDelta('0.1')
    t3 = t1 + TimeDelta('0.9')
    t4 = t1 + TimeDelta('1.0')
    t5 = t1 + TimeDelta('1.1')
    t6 = t1 + TimeDelta('1.9')
    t7 = t1 + TimeDelta('2.0')
    t8 = t1 + TimeDelta('2.1')
    
    self.assertEqual(t0.get_utc_tai_offset(), -10)
    self.assertEqual(t1.get_utc_tai_offset(), -10)
    self.assertEqual(t2.get_utc_tai_offset(), -10)
    self.assertEqual(t3.get_utc_tai_offset(), -10)
    self.assertEqual(t4.get_utc_tai_offset(), -11)
    self.assertEqual(t5.get_utc_tai_offset(), -11)
    self.assertEqual(t6.get_utc_tai_offset(), -11)
    self.assertEqual(t7.get_utc_tai_offset(), -11)
    self.assertEqual(t8.get_utc_tai_offset(), -11)
    
    t1 = TimeInstant(TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['start_instant'])
    t0 = t1 - TimeDelta('0.1')
    t2 = t1 + TimeDelta('0.1')
    t3 = t1 + TimeDelta('0.9')
    t4 = t1 + TimeDelta('1.0')
    t5 = t1 + TimeDelta('1.1')
    t6 = t1 + TimeDelta('1.9')
    t7 = t1 + TimeDelta('2.0')
    t8 = t1 + TimeDelta('2.1')
    
    self.assertEqual(t0.get_utc_tai_offset(), -36)
    self.assertEqual(t1.get_utc_tai_offset(), -36)
    self.assertEqual(t2.get_utc_tai_offset(), -36)
    self.assertEqual(t3.get_utc_tai_offset(), -36)
    self.assertEqual(t4.get_utc_tai_offset(), -37)
    self.assertEqual(t5.get_utc_tai_offset(), -37)
    self.assertEqual(t6.get_utc_tai_offset(), -37)
    self.assertEqual(t7.get_utc_tai_offset(), -37)
    self.assertEqual(t8.get_utc_tai_offset(), -37)
  
  def test_now(self):
    now = TimeInstant.now()
    current_unix_time_ns = time_ns()
    current_datetime = datetime.datetime.now(datetime.UTC)
    
    now_unix_time_ns = now.to_unix_timestamp()[0] * FixedPrec('1000000000')
    # checks if 3 milliseconds off
    self.assertTrue(abs(now_unix_time_ns - current_unix_time_ns) <= 3_000_000, f'{now_unix_time_ns} {current_unix_time_ns}')
    
    now_date_tuple = now.to_date_tuple_utc()
    self.assertEqual(
      (
        *now_date_tuple[:6],
        int(now_date_tuple[6] * 1_000_000),
      ),
      (
        current_datetime.year,
        current_datetime.month,
        current_datetime.day,
        current_datetime.hour,
        current_datetime.minute,
        current_datetime.second,
        current_datetime.microsecond,
      )
    )
  
  def test_fixedprec_offset_to_str(self):
    # test inverse func as well
    ...
  
  def test_to_format_string_tai(self):
    time_instant = TimeInstant.from_date_tuple_tai(2024, 4, 14, 13, 2, 3, FixedPrec('0.45678913'))
    self.assertEqual(
      time_instant.to_format_string_tai('a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I J:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:456789 H:13 I:01 J:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:+00:00:37 Z:Time Atomic International %:% str:test'
    )
    time_instant_2 = TimeInstant.from_date_tuple_tai(2024, 4, 15, 13, 2, 3, FixedPrec('0.45678913'))
    self.assertEqual(
      time_instant_2.to_format_string_tai('U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_utc(self):
    ...
  
  def test_from_format_string_tai(self):
    ...
  
  def test_from_format_string_utc(self):
    ...
