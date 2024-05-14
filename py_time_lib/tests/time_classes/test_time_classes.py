from datetime import datetime, timedelta, timezone, UTC
from math import trunc
from time import time_ns, struct_time
from unittest import TestCase

from ... import FixedPrec, GregorianDate, TimeDelta, TimeZone, TimeInstant, TimeUnmappableError, LeapSmearPlan, LeapSmearSingle, LeapBasis, SmearType
from ...data_py.leap_seconds import NOMINAL_SECS_PER_DAY
from ... import TIMEZONES

class TestTimeClasses(TestCase):
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
    self.assertEqual(repr(TimeDelta(FixedPrec(1000))), 'TimeDelta(FixedPrec(1000))')
    self.assertEqual(repr(TimeDelta(FixedPrec(-1000))), 'TimeDelta(FixedPrec(-1000))')
    self.assertEqual(repr(TimeDelta(FixedPrec(0))), 'TimeDelta(FixedPrec(0))')
  
  def test_time_instant_repr(self):
    self.assertEqual(repr(TimeInstant(FixedPrec(1000))), 'TimeInstant(FixedPrec(1000))')
    self.assertEqual(repr(TimeInstant(FixedPrec(-1000))), 'TimeInstant(FixedPrec(-1000))')
    self.assertEqual(repr(TimeInstant(FixedPrec(0))), 'TimeInstant(FixedPrec(0))')
  
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
    
    self.assertEqual(str(FixedPrec(4) * TimeDelta(FixedPrec(3))), 'TD+12')
    with self.assertRaises(TypeError):
      self.assertEqual(FixedPrec(3) / TimeDelta(FixedPrec(3)), TimeDelta(FixedPrec(1)))
  
  def test_time_instant_basic_ops(self):
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) + TimeDelta(FixedPrec(3))), 'T+1003')
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) - TimeDelta(FixedPrec(3))), 'T+997')
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) - TimeInstant(FixedPrec(993))), 'TD+7')
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) + TimeDelta(FixedPrec('0.1'))), 'T+1000.1')
    
    self.assertEqual(str(TimeDelta(FixedPrec(3)) + TimeInstant(FixedPrec(1000))), 'T+1003')
  
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
    self.assertEqual(t0.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t1.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t2.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t3.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t4.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t5.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t6.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t7.to_secs_since_epoch_utc(), (
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
    self.assertEqual(t8.to_secs_since_epoch_utc(), (
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
      self.assertEqual(t0.to_secs_since_epoch_utc(), (
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
      self.assertEqual(t1.to_secs_since_epoch_utc(), (
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
      self.assertEqual(t2.to_secs_since_epoch_utc(), (
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
      self.assertEqual(t3.to_secs_since_epoch_utc(), (
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
      self.assertEqual(t4.to_secs_since_epoch_utc(), (
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
      self.assertEqual(t5.to_secs_since_epoch_utc(), (
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
      self.assertEqual(instant, TimeInstant.from_secs_since_epoch_utc(*instant.to_secs_since_epoch_utc()))
    
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
      utc_before_neg_leap = instant_before_neg_leap.to_secs_since_epoch_utc()[0]
      
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap, round_invalid_time_upwards = True),
        instant_before_neg_leap
      )
      #print('\n'.join([repr(i) for i in TimeInstant.UTC_TO_TAI_OFFSET_TABLE]))
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('0.1'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('0.2'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('1.0'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('1.1'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('1.2'), round_invalid_time_upwards = True),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.2'))
      )
      
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap, round_invalid_time_upwards = False),
        instant_before_neg_leap
      )
      
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('0.1'), round_invalid_time_upwards = False)
      
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('0.2'), round_invalid_time_upwards = False)
      
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('1.0'), round_invalid_time_upwards = False)
      
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('1.1'), round_invalid_time_upwards = False),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.1'))
      )
      self.assertEqual(
        TimeInstant.from_secs_since_epoch_utc(utc_before_neg_leap + FixedPrec('1.2'), round_invalid_time_upwards = False),
        instant_before_neg_leap + TimeDelta(FixedPrec('0.2'))
      )
  
  def test_tai_utc_tuple_leap_secs(self):
    with TimeInstant._temp_add_leap_secs(27, [
        ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1)),
        ('2018-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-2)),
        ('2018-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(2)),
      ]):
      
      leap_normal_pos_midnight = TimeInstant.from_secs_since_epoch_utc(GregorianDate(2017, 1, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_normal_neg_midnight = TimeInstant.from_secs_since_epoch_utc(GregorianDate(2018, 1, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_big_pos_midnight = TimeInstant.from_secs_since_epoch_utc(GregorianDate(2018, 7, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_big_neg_midnight = TimeInstant.from_secs_since_epoch_utc(GregorianDate(2019, 1, 1).days_since_epoch * TimeInstant.NOMINAL_SECS_PER_DAY)
      
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
  
  def test_jd_utc(self):
    instant = TimeInstant.from_date_tuple_tai(2024, 4, 9, 20, 30, 54, 0)
    jd_tai = instant.to_julian_date_tai()
    jd_utc = instant.to_julian_date_utc()
    rjd_tai = instant.to_reduced_julian_date_tai()
    rjd_utc = instant.to_reduced_julian_date_utc()
    mjd_tai = instant.to_modified_julian_date_tai()
    mjd_utc = instant.to_modified_julian_date_utc()
    self.assertAlmostEqual(jd_utc.julian_date - jd_tai, FixedPrec('-37') / 86400, 5)
    self.assertAlmostEqual(rjd_utc.reduced_julian_date - rjd_tai, FixedPrec('-37') / 86400, 5)
    self.assertAlmostEqual(mjd_utc.modified_julian_date - mjd_tai, FixedPrec('-37') / 86400, 5)
    self.assertAlmostEqual(TimeInstant.from_julian_date_utc(*jd_utc).time, instant.time, 1)
    self.assertAlmostEqual(TimeInstant.from_reduced_julian_date_utc(*rjd_utc).time, instant.time, 1)
    self.assertAlmostEqual(TimeInstant.from_modified_julian_date_utc(*mjd_utc).time, instant.time, 1)
    
    with TimeInstant._temp_add_leap_sec(27, ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1))):
      instant_pos_leap_first_fold = TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 60, FixedPrec('0.5'))
      instant_pos_leap_second_fold = TimeInstant.from_date_tuple_utc(2017, 1, 1, 0, 0, 0, FixedPrec('0.5'))
      instant_neg_leap_end = TimeInstant.from_date_tuple_utc(2018, 1, 1, 0, 0, 0, 0)
      
      pos_leap_first_fold_jd_tai = instant_pos_leap_first_fold.to_julian_date_tai()
      pos_leap_first_fold_jd_utc = instant_pos_leap_first_fold.to_julian_date_utc()
      pos_leap_first_fold_rjd_tai = instant_pos_leap_first_fold.to_reduced_julian_date_tai()
      pos_leap_first_fold_rjd_utc = instant_pos_leap_first_fold.to_reduced_julian_date_utc()
      pos_leap_first_fold_mjd_tai = instant_pos_leap_first_fold.to_modified_julian_date_tai()
      pos_leap_first_fold_mjd_utc = instant_pos_leap_first_fold.to_modified_julian_date_utc()
      self.assertAlmostEqual(pos_leap_first_fold_jd_utc.julian_date - pos_leap_first_fold_jd_tai, FixedPrec('-36') / 86400, 5)
      self.assertAlmostEqual(pos_leap_first_fold_rjd_utc.reduced_julian_date - pos_leap_first_fold_rjd_tai, FixedPrec('-36') / 86400, 5)
      self.assertAlmostEqual(pos_leap_first_fold_mjd_utc.modified_julian_date - pos_leap_first_fold_mjd_tai, FixedPrec('-36') / 86400, 5)
      self.assertAlmostEqual(TimeInstant.from_julian_date_utc(*pos_leap_first_fold_jd_utc).time, instant_pos_leap_first_fold.time, 0)
      self.assertAlmostEqual(TimeInstant.from_reduced_julian_date_utc(*pos_leap_first_fold_rjd_utc).time, instant_pos_leap_first_fold.time, 0)
      self.assertAlmostEqual(TimeInstant.from_modified_julian_date_utc(*pos_leap_first_fold_mjd_utc).time, instant_pos_leap_first_fold.time, 0)
      
      pos_leap_second_fold_jd_tai = instant_pos_leap_second_fold.to_julian_date_tai()
      pos_leap_second_fold_jd_utc = instant_pos_leap_second_fold.to_julian_date_utc()
      pos_leap_second_fold_rjd_tai = instant_pos_leap_second_fold.to_reduced_julian_date_tai()
      pos_leap_second_fold_rjd_utc = instant_pos_leap_second_fold.to_reduced_julian_date_utc()
      pos_leap_second_fold_mjd_tai = instant_pos_leap_second_fold.to_modified_julian_date_tai()
      pos_leap_second_fold_mjd_utc = instant_pos_leap_second_fold.to_modified_julian_date_utc()
      self.assertAlmostEqual(pos_leap_second_fold_jd_utc.julian_date - pos_leap_second_fold_jd_tai, FixedPrec('-37') / 86400, 5)
      self.assertAlmostEqual(pos_leap_second_fold_rjd_utc.reduced_julian_date - pos_leap_second_fold_rjd_tai, FixedPrec('-37') / 86400, 5)
      self.assertAlmostEqual(pos_leap_second_fold_mjd_utc.modified_julian_date - pos_leap_second_fold_mjd_tai, FixedPrec('-37') / 86400, 5)
      self.assertAlmostEqual(TimeInstant.from_julian_date_utc(*pos_leap_second_fold_jd_utc).time, instant_pos_leap_second_fold.time, 0)
      self.assertAlmostEqual(TimeInstant.from_reduced_julian_date_utc(*pos_leap_second_fold_rjd_utc).time, instant_pos_leap_second_fold.time, 0)
      self.assertAlmostEqual(TimeInstant.from_modified_julian_date_utc(*pos_leap_second_fold_mjd_utc).time, instant_pos_leap_second_fold.time, 0)
      
      neg_leap_end_jd_tai = instant_neg_leap_end.to_julian_date_tai()
      neg_leap_end_jd_utc = instant_neg_leap_end.to_julian_date_utc()
      neg_leap_end_jd_utc_invalid = neg_leap_end_jd_utc.julian_date - (FixedPrec('0.5') / 86400), False
      neg_leap_end_rjd_tai = instant_neg_leap_end.to_reduced_julian_date_tai()
      neg_leap_end_rjd_utc = instant_neg_leap_end.to_reduced_julian_date_utc()
      neg_leap_end_rjd_utc_invalid = neg_leap_end_rjd_utc.reduced_julian_date - (FixedPrec('0.5') / 86400), False
      neg_leap_end_mjd_tai = instant_neg_leap_end.to_modified_julian_date_tai()
      neg_leap_end_mjd_utc = instant_neg_leap_end.to_modified_julian_date_utc()
      neg_leap_end_mjd_utc_invalid = neg_leap_end_mjd_utc.modified_julian_date - (FixedPrec('0.5') / 86400), False
      self.assertAlmostEqual(neg_leap_end_jd_utc.julian_date - neg_leap_end_jd_tai, FixedPrec('-36') / 86400, 5)
      self.assertAlmostEqual(neg_leap_end_rjd_utc.reduced_julian_date - neg_leap_end_rjd_tai, FixedPrec('-36') / 86400, 5)
      self.assertAlmostEqual(neg_leap_end_mjd_utc.modified_julian_date - neg_leap_end_mjd_tai, FixedPrec('-36') / 86400, 5)
      self.assertAlmostEqual(TimeInstant.from_julian_date_utc(*neg_leap_end_jd_utc).time, instant_neg_leap_end.time, 1)
      self.assertAlmostEqual(TimeInstant.from_reduced_julian_date_utc(*neg_leap_end_rjd_utc).time, instant_neg_leap_end.time, 1)
      self.assertAlmostEqual(TimeInstant.from_modified_julian_date_utc(*neg_leap_end_mjd_utc).time, instant_neg_leap_end.time, 1)
      self.assertAlmostEqual(TimeInstant.from_julian_date_utc(*neg_leap_end_jd_utc_invalid).time, instant_neg_leap_end.time, 1)
      self.assertAlmostEqual(TimeInstant.from_reduced_julian_date_utc(*neg_leap_end_rjd_utc_invalid).time, instant_neg_leap_end.time, 1)
      self.assertAlmostEqual(TimeInstant.from_modified_julian_date_utc(*neg_leap_end_mjd_utc_invalid).time, instant_neg_leap_end.time, 1)
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_julian_date_utc(*neg_leap_end_jd_utc_invalid, round_invalid_time_upwards = False)
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_reduced_julian_date_utc(*neg_leap_end_rjd_utc_invalid, round_invalid_time_upwards = False)
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_modified_julian_date_utc(*neg_leap_end_mjd_utc_invalid, round_invalid_time_upwards = False)
  
  def test_jd_mono(self):
    instant = TimeInstant.from_date_tuple_tai(2024, 4, 9, 20, 30, 54, 0)
    jd_tai = instant.to_julian_date_tai()
    jd_tt = instant.to_julian_date_mono(TimeInstant.TIME_SCALES.TT)
    rjd_tai = instant.to_reduced_julian_date_tai()
    rjd_tt = instant.to_reduced_julian_date_mono(TimeInstant.TIME_SCALES.TT)
    mjd_tai = instant.to_modified_julian_date_tai()
    mjd_tt = instant.to_modified_julian_date_mono(TimeInstant.TIME_SCALES.TT)
    self.assertAlmostEqual(jd_tt - jd_tai, FixedPrec('32.184') / 86400, 5)
    self.assertAlmostEqual(rjd_tt - rjd_tai, FixedPrec('32.184') / 86400, 5)
    self.assertAlmostEqual(mjd_tt - mjd_tai, FixedPrec('32.184') / 86400, 5)
    self.assertAlmostEqual(TimeInstant.from_julian_date_mono(TimeInstant.TIME_SCALES.TT, jd_tt).time, instant.time, 1)
    self.assertAlmostEqual(TimeInstant.from_reduced_julian_date_mono(TimeInstant.TIME_SCALES.TT, rjd_tt).time, instant.time, 1)
    self.assertAlmostEqual(TimeInstant.from_modified_julian_date_mono(TimeInstant.TIME_SCALES.TT, mjd_tt).time, instant.time, 1)
  
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
    current_datetime = datetime.now(UTC)
    
    now_unix_time_ns = now.to_unix_timestamp()[0] * FixedPrec('1000000000')
    # checks if 3 milliseconds off
    self.assertTrue(abs(now_unix_time_ns - current_unix_time_ns) <= 3_000_000, f'{now_unix_time_ns} {current_unix_time_ns}')
    
    now_date_tuple = now.to_date_tuple_utc()
    now_datetime = datetime(*now_date_tuple[:6], int(now_date_tuple[6] * 1_000_000), UTC)
    
    self.assertTrue(abs(now_datetime - current_datetime) <= timedelta(microseconds = 1015), abs(now_datetime - current_datetime))
  
  def test_hash_timedelta(self):
    self.assertEqual(hash(TimeDelta(3)), hash(('TimeDelta', FixedPrec(3))))
    self.assertEqual(hash(TimeDelta(3)), hash(('TimeDelta', 3)))
  
  def test_hash_timeinstant(self):
    self.assertEqual(hash(TimeInstant(3)), hash(('TimeInstant', FixedPrec(3))))
    self.assertEqual(hash(TimeInstant(3)), hash(('TimeInstant', 3)))
  
  def test_to_timedelta(self):
    self.assertEqual(TimeDelta(FixedPrec('3.5')).to_datetime_timedelta(), timedelta(seconds = 3, milliseconds = 500))
  
  def test_to_datetime_basic(self):
    self.assertEqual(
      TimeInstant.from_date_tuple_utc(2024, 4, 19, 13, 1, 1, 0).to_datetime(),
      datetime(2024, 4, 19, 13, 1, 1, 0, UTC)
    )
    self.assertEqual(
      TimeInstant.from_datetime(datetime(2024, 4, 19, 13, 1, 1, 0, UTC)).to_date_tuple_utc(),
      (2024, 4, 19, 13, 1, 1, 0)
    )
    self.assertEqual(
      TimeInstant.from_date_tuple_utc(2024, 4, 19, 13, 1, 1, FixedPrec('0.5')).to_datetime(),
      datetime(2024, 4, 19, 13, 1, 1, 500_000, UTC)
    )
    self.assertEqual(
      TimeInstant.from_datetime(datetime(2024, 4, 19, 13, 1, 1, 500_000, UTC)).to_date_tuple_utc(),
      (2024, 4, 19, 13, 1, 1, FixedPrec('0.5'))
    )
    self.assertEqual(
      TimeInstant(datetime(2024, 4, 19, 13, 1, 1, 500_000, UTC)).to_date_tuple_utc(),
      (2024, 4, 19, 13, 1, 1, FixedPrec('0.5'))
    )

    utc_plus_1 = timezone(timedelta(hours = 1))
    
    self.assertEqual(
      TimeInstant.from_datetime(datetime(2024, 4, 19, 13, 1, 1, 500_000, utc_plus_1)).to_date_tuple_utc(),
      (2024, 4, 19, 12, 1, 1, FixedPrec('0.5'))
    )
  
  def test_to_datetime_leap_sec(self):
    last_leap_index = 53
    last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['start_instant']
    t1 = TimeInstant(last_leap_start)
    t0 = t1 - TimeDelta('0.1')
    t2 = t1 + TimeDelta('0.1')
    t3 = t1 + TimeDelta('0.9')
    t4 = t1 + TimeDelta('1.0')
    t5 = t1 + TimeDelta('1.1')
    t6 = t1 + TimeDelta('1.9')
    t7 = t1 + TimeDelta('2.0')
    t8 = t1 + TimeDelta('2.1')
    
    self.assertEqual(t0.to_datetime(), datetime(2016, 12, 31, 23, 59, 59, 900_000, UTC))
    self.assertEqual(t1.to_datetime(), datetime(2017, 1,  1,  0,  0,  0,  0,       UTC))
    self.assertEqual(t2.to_datetime(), datetime(2017, 1,  1,  0,  0,  0,  0,       UTC))
    self.assertEqual(t3.to_datetime(), datetime(2017, 1,  1,  0,  0,  0,  0,       UTC))
    self.assertEqual(t4.to_datetime(), datetime(2017, 1,  1,  0,  0,  0,  0,       UTC))
    self.assertEqual(t5.to_datetime(), datetime(2017, 1,  1,  0,  0,  0,  100_000, UTC))
    self.assertEqual(t6.to_datetime(), datetime(2017, 1,  1,  0,  0,  0,  900_000, UTC))
    self.assertEqual(t7.to_datetime(), datetime(2017, 1,  1,  0,  0,  1,  0,       UTC))
    self.assertEqual(t8.to_datetime(), datetime(2017, 1,  1,  0,  0,  1,  100_000, UTC))
  
  def test_from_timedelta(self):
    self.assertEqual(TimeDelta.from_datetime_timedelta(timedelta(seconds = 1, microseconds = 13)), TimeDelta(FixedPrec('1.000013')))
    self.assertEqual(TimeDelta.from_datetime_timedelta(timedelta(seconds = 0, microseconds = 0)), TimeDelta(FixedPrec(0)))
    self.assertEqual(TimeDelta.from_datetime_timedelta(timedelta(seconds = -2, microseconds = -15)), TimeDelta(FixedPrec('-2.000015')))
    self.assertEqual(TimeDelta(timedelta(seconds = 1, microseconds = 13)), TimeDelta(FixedPrec('1.000013')))
    self.assertEqual(TimeDelta(timedelta(seconds = 0, microseconds = 0)), TimeDelta(FixedPrec(0)))
    self.assertEqual(TimeDelta(timedelta(seconds = -2, microseconds = -15)), TimeDelta(FixedPrec('-2.000015')))
  
  def test_no_attributes(self):
    with self.assertRaises(AttributeError):
      d1 = TimeDelta(2024)
      d1.prop = False
    with self.assertRaises(AttributeError):
      d1 = TimeInstant(2024)
      d1.prop = False
    with self.assertRaises(AttributeError):
      d1 = TimeZone(2)
      d1.prop = False
  
  def test_timezone_fixed(self):
    tz = TimeZone(3_600)
    instant = TimeInstant.from_date_tuple_utc(2024, 4, 21, 23, 1, 2, FixedPrec('0.3'))
    instant_copy = TimeInstant.from_date_tuple_tz(tz, 2024, 4, 22, 0, 1, 2, FixedPrec('0.3'))
    self.assertEqual(instant.to_date_tuple_tz(tz), (2024, 4, 22, 0, 1, 2, FixedPrec('0.3'), False))
    self.assertEqual(instant, instant_copy)
  
  def test_timezone_variable(self):
    tz = TimeZone(
      1 * 3_600,
      initial_offset = {
        'utc_offset': 1 * 3_600,
        'abbreviation': 'Test1',
      },
      later_offsets = (
        {
          'offset_day_mode': TimeZone.OffsetDayMode.MONTH_AND_DAY,
          'month': 4,
          'day': 15,
          'start_time_in_day': 5 * 3_600,
          'utc_offset': 2 * 3_600,
          'abbreviation': 'Test2',
        },
        {
          'offset_day_mode': TimeZone.OffsetDayMode.MONTH_WEEK_DAY,
          'month': 8,
          'week': 1,
          'day_in_week': 2,
          'from_month_end': True,
          'start_time_in_day': 30 * 60,
          'utc_offset': 1 * 3_600,
          'abbreviation': 'Test3',
        },
      )
    )
    
    def test(instant: TimeInstant, utc_tuple, tz_tuple, offset, abbr):
      utc_tuple = *utc_tuple[:6], FixedPrec(utc_tuple[6])
      tz_tuple = *tz_tuple[:6], FixedPrec(tz_tuple[6]), tz_tuple[7]
      inst_from_utc = TimeInstant.from_date_tuple_utc(*utc_tuple)
      inst_from_tz = TimeInstant.from_date_tuple_tz(tz, *tz_tuple)
      self.assertEqual(instant, inst_from_utc)
      self.assertEqual(instant, inst_from_tz)
      self.assertEqual(instant.to_date_tuple_utc(), utc_tuple)
      self.assertEqual(instant.to_date_tuple_tz(tz), tz_tuple)
      self.assertEqual(instant.get_current_tz_offset(tz), (FixedPrec(offset), abbr))
    
    def test2(instant: TimeInstant, tz_tuple, rounded_utc_tuple, rounded_tz_tuple):
      rounded_utc_tuple = *rounded_utc_tuple[:6], FixedPrec(rounded_utc_tuple[6])
      tz_tuple = *tz_tuple[:6], FixedPrec(tz_tuple[6]), tz_tuple[7]
      rounded_tz_tuple = *rounded_tz_tuple[:6], FixedPrec(rounded_tz_tuple[6]), rounded_tz_tuple[7]
      inst_from_utc = TimeInstant.from_date_tuple_utc(*rounded_utc_tuple)
      inst_from_tz = TimeInstant.from_date_tuple_tz(tz, *tz_tuple)
      with self.assertRaises(TimeUnmappableError):
        TimeInstant.from_date_tuple_tz(tz, *tz_tuple, round_invalid_dst_time_upwards = False)
      self.assertEqual(instant, inst_from_utc)
      self.assertEqual(instant, inst_from_tz)
      self.assertEqual(instant.to_date_tuple_utc(), rounded_utc_tuple)
      self.assertEqual(instant.to_date_tuple_tz(tz), rounded_tz_tuple)
    
    ta4 = TimeInstant.from_date_tuple_utc(2023, 4, 15, 4, 0, 0, FixedPrec(0))
    ta0 = ta4 - TimeDelta(FixedPrec('3600.1'))
    ta1 = ta4 - TimeDelta(FixedPrec('3600'))
    ta2 = ta4 - TimeDelta(FixedPrec('3599.9'))
    ta3 = ta4 - TimeDelta(FixedPrec('0.1'))
    ta5 = ta4 + TimeDelta(FixedPrec('0.1'))
    ta6 = ta4 + TimeDelta(FixedPrec('3599.9'))
    ta7 = ta4 + TimeDelta(FixedPrec('3600'))
    ta8 = ta4 + TimeDelta(FixedPrec('3600.1'))
    
    test(ta0, (2023, 4, 15, 2, 59, 59, '0.9'), (2023, 4, 15, 3, 59, 59, '0.9', False), '3600', 'Test1')
    test(ta1, (2023, 4, 15, 3, 0,  0,  '0'  ), (2023, 4, 15, 4, 0,  0,  '0',   False), '3600', 'Test1')
    test(ta2, (2023, 4, 15, 3, 0,  0,  '0.1'), (2023, 4, 15, 4, 0,  0,  '0.1', False), '3600', 'Test1')
    test(ta3, (2023, 4, 15, 3, 59, 59, '0.9'), (2023, 4, 15, 4, 59, 59, '0.9', False), '3600', 'Test1')
    test(ta4, (2023, 4, 15, 4, 0,  0,  '0'  ), (2023, 4, 15, 6, 0,  0,  '0',   False), '7200', 'Test2')
    test(ta5, (2023, 4, 15, 4, 0,  0,  '0.1'), (2023, 4, 15, 6, 0,  0,  '0.1', False), '7200', 'Test2')
    test(ta6, (2023, 4, 15, 4, 59, 59, '0.9'), (2023, 4, 15, 6, 59, 59, '0.9', False), '7200', 'Test2')
    test(ta7, (2023, 4, 15, 5, 0,  0,  '0'  ), (2023, 4, 15, 7, 0,  0,  '0',   False), '7200', 'Test2')
    test(ta8, (2023, 4, 15, 5, 0,  0,  '0.1'), (2023, 4, 15, 7, 0,  0,  '0.1', False), '7200', 'Test2')
    
    test2(ta4, (2023, 4, 15, 5, 0,  0,  '0',   False), (2023, 4, 15, 4, 0,  0,  '0'  ), (2023, 4, 15, 6, 0,  0,  '0',   False))
    test2(ta4, (2023, 4, 15, 5, 0,  0,  '0.1', False), (2023, 4, 15, 4, 0,  0,  '0'  ), (2023, 4, 15, 6, 0,  0,  '0',   False))
    test2(ta4, (2023, 4, 15, 5, 59, 59, '0.9', False), (2023, 4, 15, 4, 0,  0,  '0'  ), (2023, 4, 15, 6, 0,  0,  '0',   False))
    
    tb4 = TimeInstant.from_date_tuple_utc(2023, 8, 28, 22, 30, 0, FixedPrec(0))
    tb0 = tb4 - TimeDelta(FixedPrec('3600.1'))
    tb1 = tb4 - TimeDelta(FixedPrec('3600'))
    tb2 = tb4 - TimeDelta(FixedPrec('3599.9'))
    tb3 = tb4 - TimeDelta(FixedPrec('0.1'))
    tb5 = tb4 + TimeDelta(FixedPrec('0.1'))
    tb6 = tb4 + TimeDelta(FixedPrec('3599.9'))
    tb7 = tb4 + TimeDelta(FixedPrec('3600'))
    tb8 = tb4 + TimeDelta(FixedPrec('3600.1'))
    tb9 = tb4 + TimeDelta(FixedPrec('7199.9'))
    tb10 = tb4 + TimeDelta(FixedPrec('7200'))
    tb11 = tb4 + TimeDelta(FixedPrec('7200.1'))
    
    test(tb0,  (2023, 8, 28, 21, 29, 59, '0.9'), (2023, 8, 28, 23, 29, 59, '0.9', False), '7200', 'Test2')
    test(tb1,  (2023, 8, 28, 21, 30, 0,  '0'  ), (2023, 8, 28, 23, 30, 0,  '0',   False), '7200', 'Test2')
    test(tb2,  (2023, 8, 28, 21, 30, 0,  '0.1'), (2023, 8, 28, 23, 30, 0,  '0.1', False), '7200', 'Test2')
    test(tb3,  (2023, 8, 28, 22, 29, 59, '0.9'), (2023, 8, 29, 0,  29, 59, '0.9', False), '7200', 'Test2')
    test(tb4,  (2023, 8, 28, 22, 30, 0,  '0'  ), (2023, 8, 28, 23, 30, 0,  '0',   True ), '3600', 'Test3')
    test(tb5,  (2023, 8, 28, 22, 30, 0,  '0.1'), (2023, 8, 28, 23, 30, 0,  '0.1', True ), '3600', 'Test3')
    test(tb6,  (2023, 8, 28, 23, 29, 59, '0.9'), (2023, 8, 29, 0,  29, 59, '0.9', True ), '3600', 'Test3')
    test(tb7,  (2023, 8, 28, 23, 30, 0,  '0'  ), (2023, 8, 29, 0,  30, 0,  '0',   False), '3600', 'Test3')
    test(tb8,  (2023, 8, 28, 23, 30, 0,  '0.1'), (2023, 8, 29, 0,  30, 0,  '0.1', False), '3600', 'Test3')
    test(tb9,  (2023, 8, 29, 0,  29, 59, '0.9'), (2023, 8, 29, 1,  29, 59, '0.9', False), '3600', 'Test3')
    test(tb10, (2023, 8, 29, 0,  30, 0,  '0'  ), (2023, 8, 29, 1,  30, 0,  '0',   False), '3600', 'Test3')
    test(tb11, (2023, 8, 29, 0,  30, 0,  '0.1'), (2023, 8, 29, 1,  30, 0,  '0.1', False), '3600', 'Test3')
    
    tc4 = TimeInstant.from_date_tuple_utc(2024, 4, 15, 4, 0, 0, FixedPrec(0))
    tc0 = tc4 - TimeDelta(FixedPrec('3600.1'))
    tc1 = tc4 - TimeDelta(FixedPrec('3600'))
    tc2 = tc4 - TimeDelta(FixedPrec('3599.9'))
    tc3 = tc4 - TimeDelta(FixedPrec('0.1'))
    tc5 = tc4 + TimeDelta(FixedPrec('0.1'))
    tc6 = tc4 + TimeDelta(FixedPrec('3599.9'))
    tc7 = tc4 + TimeDelta(FixedPrec('3600'))
    tc8 = tc4 + TimeDelta(FixedPrec('3600.1'))
    
    test(tc0, (2024, 4, 15, 2, 59, 59, '0.9'), (2024, 4, 15, 3, 59, 59, '0.9', False), '3600', 'Test1')
    test(tc1, (2024, 4, 15, 3, 0,  0,  '0'  ), (2024, 4, 15, 4, 0,  0,  '0',   False), '3600', 'Test1')
    test(tc2, (2024, 4, 15, 3, 0,  0,  '0.1'), (2024, 4, 15, 4, 0,  0,  '0.1', False), '3600', 'Test1')
    test(tc3, (2024, 4, 15, 3, 59, 59, '0.9'), (2024, 4, 15, 4, 59, 59, '0.9', False), '3600', 'Test1')
    test(tc4, (2024, 4, 15, 4, 0,  0,  '0'  ), (2024, 4, 15, 6, 0,  0,  '0',   False), '7200', 'Test2')
    test(tc5, (2024, 4, 15, 4, 0,  0,  '0.1'), (2024, 4, 15, 6, 0,  0,  '0.1', False), '7200', 'Test2')
    test(tc6, (2024, 4, 15, 4, 59, 59, '0.9'), (2024, 4, 15, 6, 59, 59, '0.9', False), '7200', 'Test2')
    test(tc7, (2024, 4, 15, 5, 0,  0,  '0'  ), (2024, 4, 15, 7, 0,  0,  '0',   False), '7200', 'Test2')
    test(tc8, (2024, 4, 15, 5, 0,  0,  '0.1'), (2024, 4, 15, 7, 0,  0,  '0.1', False), '7200', 'Test2')
    
    test2(tc4, (2024, 4, 15, 5, 0,  0,  '0',   False), (2024, 4, 15, 4, 0,  0,  '0'  ), (2024, 4, 15, 6, 0,  0,  '0',   False))
    test2(tc4, (2024, 4, 15, 5, 0,  0,  '0.1', False), (2024, 4, 15, 4, 0,  0,  '0'  ), (2024, 4, 15, 6, 0,  0,  '0',   False))
    test2(tc4, (2024, 4, 15, 5, 59, 59, '0.9', False), (2024, 4, 15, 4, 0,  0,  '0'  ), (2024, 4, 15, 6, 0,  0,  '0',   False))
    
    td4 = TimeInstant.from_date_tuple_utc(2024, 8, 26, 22, 30, 0, FixedPrec(0))
    td0 = td4 - TimeDelta(FixedPrec('3600.1'))
    td1 = td4 - TimeDelta(FixedPrec('3600'))
    td2 = td4 - TimeDelta(FixedPrec('3599.9'))
    td3 = td4 - TimeDelta(FixedPrec('0.1'))
    td5 = td4 + TimeDelta(FixedPrec('0.1'))
    td6 = td4 + TimeDelta(FixedPrec('3599.9'))
    td7 = td4 + TimeDelta(FixedPrec('3600'))
    td8 = td4 + TimeDelta(FixedPrec('3600.1'))
    td9 = td4 + TimeDelta(FixedPrec('7199.9'))
    td10 = td4 + TimeDelta(FixedPrec('7200'))
    td11 = td4 + TimeDelta(FixedPrec('7200.1'))
    
    test(td0,  (2024, 8, 26, 21, 29, 59, '0.9'), (2024, 8, 26, 23, 29, 59, '0.9', False), '7200', 'Test2')
    test(td1,  (2024, 8, 26, 21, 30, 0,  '0'  ), (2024, 8, 26, 23, 30, 0,  '0',   False), '7200', 'Test2')
    test(td2,  (2024, 8, 26, 21, 30, 0,  '0.1'), (2024, 8, 26, 23, 30, 0,  '0.1', False), '7200', 'Test2')
    test(td3,  (2024, 8, 26, 22, 29, 59, '0.9'), (2024, 8, 27, 0,  29, 59, '0.9', False), '7200', 'Test2')
    test(td4,  (2024, 8, 26, 22, 30, 0,  '0'  ), (2024, 8, 26, 23, 30, 0,  '0',   True ), '3600', 'Test3')
    test(td5,  (2024, 8, 26, 22, 30, 0,  '0.1'), (2024, 8, 26, 23, 30, 0,  '0.1', True ), '3600', 'Test3')
    test(td6,  (2024, 8, 26, 23, 29, 59, '0.9'), (2024, 8, 27, 0,  29, 59, '0.9', True ), '3600', 'Test3')
    test(td7,  (2024, 8, 26, 23, 30, 0,  '0'  ), (2024, 8, 27, 0,  30, 0,  '0',   False), '3600', 'Test3')
    test(td8,  (2024, 8, 26, 23, 30, 0,  '0.1'), (2024, 8, 27, 0,  30, 0,  '0.1', False), '3600', 'Test3')
    test(td9,  (2024, 8, 27, 0,  29, 59, '0.9'), (2024, 8, 27, 1,  29, 59, '0.9', False), '3600', 'Test3')
    test(td10, (2024, 8, 27, 0,  30, 0,  '0'  ), (2024, 8, 27, 1,  30, 0,  '0',   False), '3600', 'Test3')
    test(td11, (2024, 8, 27, 0,  30, 0,  '0.1'), (2024, 8, 27, 1,  30, 0,  '0.1', False), '3600', 'Test3')
  
  def test_timezone_leap(self):
    with TimeInstant._temp_add_leap_sec(27, ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1))):
      tz = TimeZone(
        1 * 3_600,
        initial_offset = {
          'utc_offset': 1 * 3_600,
          'abbreviation': 'Test1',
        },
        later_offsets = (
          {
            'offset_day_mode': TimeZone.OffsetDayMode.MONTH_AND_DAY,
            'month': 4,
            'day': 15,
            'start_time_in_day': 5 * 3_600,
            'utc_offset': 2 * 3_600,
            'abbreviation': 'Test2',
          },
          {
            'offset_day_mode': TimeZone.OffsetDayMode.MONTH_WEEK_DAY,
            'month': 8,
            'week': 1,
            'day_in_week': 2,
            'from_month_end': True,
            'start_time_in_day': 30 * 60,
            'utc_offset': 1 * 3_600,
            'abbreviation': 'Test3',
          },
        )
      )
      
      def test(delta, utc_tuple, tz_tuple, offset, abbr):
        instant = current_instant + TimeDelta(delta)
        utc_tuple = *utc_tuple[:6], FixedPrec(utc_tuple[6])
        tz_tuple = *tz_tuple[:6], FixedPrec(tz_tuple[6]), tz_tuple[7]
        inst_from_utc = TimeInstant.from_date_tuple_utc(*utc_tuple)
        inst_from_tz = TimeInstant.from_date_tuple_tz(tz, *tz_tuple)
        self.assertEqual(instant, inst_from_utc)
        self.assertEqual(instant, inst_from_tz)
        self.assertEqual(instant.to_date_tuple_utc(), utc_tuple)
        self.assertEqual(instant.to_date_tuple_tz(tz), tz_tuple)
        self.assertEqual(instant.get_current_tz_offset(tz), (FixedPrec(offset), abbr))
      
      current_instant = TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 59, FixedPrec('0.9'))
      
      test('0',   (2016, 12, 31, 23, 59, 59, '0.9'), (2017, 1, 1, 0, 59, 59, '0.9', False), '3600', 'Test1')
      test('0.1', (2016, 12, 31, 23, 59, 60, '0'  ), (2017, 1, 1, 0, 59, 60, '0'  , False), '3600', 'Test1')
      test('0.15', (2016, 12, 31, 23, 59, 60, '0.05'), (2017, 1, 1, 0, 59, 60, '0.05', False), '3600', 'Test1')
      test('0.2', (2016, 12, 31, 23, 59, 60, '0.1'), (2017, 1, 1, 0, 59, 60, '0.1', False), '3600', 'Test1')
      test('1',   (2016, 12, 31, 23, 59, 60, '0.9'), (2017, 1, 1, 0, 59, 60, '0.9', False), '3600', 'Test1')
      test('1.1', (2017, 1,  1,  0,  0,  0,  '0'  ), (2017, 1, 1, 1, 0,  0,  '0'  , False), '3600', 'Test1')
      test('1.2', (2017, 1,  1,  0,  0,  0,  '0.1'), (2017, 1, 1, 1, 0,  0,  '0.1', False), '3600', 'Test1')
      test('2',   (2017, 1,  1,  0,  0,  0,  '0.9'), (2017, 1, 1, 1, 0,  0,  '0.9', False), '3600', 'Test1')
      test('2.1', (2017, 1,  1,  0,  0,  1,  '0'  ), (2017, 1, 1, 1, 0,  1,  '0'  , False), '3600', 'Test1')
      test('2.2', (2017, 1,  1,  0,  0,  1,  '0.1'), (2017, 1, 1, 1, 0,  1,  '0.1', False), '3600', 'Test1')
      
      current_instant = TimeInstant.from_date_tuple_utc(2017, 12, 31, 23, 59, 58, FixedPrec('0.9'))
      
      test('0',   (2017, 12, 31, 23, 59, 58, '0.9'), (2018, 1, 1, 0, 59, 58, '0.9', False), '3600', 'Test1')
      test('0.1', (2018, 1,  1,  0,  0,  0,  '0'  ), (2018, 1, 1, 1, 0,  0,  '0'  , False), '3600', 'Test1')
      test('0.2', (2018, 1,  1,  0,  0,  0,  '0.1'), (2018, 1, 1, 1, 0,  0,  '0.1', False), '3600', 'Test1')
      test('1',   (2018, 1,  1,  0,  0,  0,  '0.9'), (2018, 1, 1, 1, 0,  0,  '0.9', False), '3600', 'Test1')
      test('1.1', (2018, 1,  1,  0,  0,  1,  '0'  ), (2018, 1, 1, 1, 0,  1,  '0'  , False), '3600', 'Test1')
      test('1.2', (2018, 1,  1,  0,  0,  1,  '0.1'), (2018, 1, 1, 1, 0,  1,  '0.1', False), '3600', 'Test1')
  
  def test_struct_time(self):
    def struct_time_equals(struct1, struct2):
      self.assertEqual(struct1, struct2)
      self.assertEqual(struct1.tm_zone, struct2.tm_zone)
      self.assertEqual(struct1.tm_gmtoff, struct2.tm_gmtoff)
    
    def test_utc(utc_tuple, week_day, ordinal_date):
      is_dst = 0
      tm_zone = 'UTC'
      tm_gmtoff = 0
      instant = TimeInstant.from_date_tuple_utc(*utc_tuple, 0)
      struct_time_obj = struct_time((*utc_tuple, week_day, ordinal_date, is_dst), {'tm_zone': tm_zone, 'tm_gmtoff': tm_gmtoff})
      struct_time_equals(
        instant.to_struct_time(),
        struct_time_obj
      )
      self.assertEqual(
        instant,
        TimeInstant.from_struct_time(struct_time_obj)
      )
      self.assertEqual(
        instant,
        TimeInstant(struct_time_obj)
      )
    
    test_utc((2016, 12, 30, 23, 59, 58), 4, 365)
    test_utc((2016, 12, 30, 23, 59, 59), 4, 365)
    test_utc((2016, 12, 31, 0,  0,  0 ), 5, 366)
    test_utc((2016, 12, 31, 22, 59, 58), 5, 366)
    test_utc((2016, 12, 31, 22, 59, 59), 5, 366)
    test_utc((2016, 12, 31, 23, 0,  0 ), 5, 366)
    test_utc((2016, 12, 31, 23, 59, 58), 5, 366)
    test_utc((2016, 12, 31, 23, 59, 59), 5, 366)
    test_utc((2016, 12, 31, 23, 59, 60), 5, 366)
    test_utc((2017, 1,  1,  0,  0,  0 ), 6, 1  )
    test_utc((2017, 1,  1,  0,  0,  1 ), 6, 1  )
    
    tz = TimeZone(
      1 * 3_600,
      initial_offset = {
        'utc_offset': 1 * 3_600,
        'abbreviation': 'Test1',
      },
      later_offsets = (
        {
          'offset_day_mode': TimeZone.OffsetDayMode.MONTH_AND_DAY,
          'month': 4,
          'day': 15,
          'start_time_in_day': 5 * 3_600,
          'utc_offset': 2 * 3_600,
          'abbreviation': 'Test2',
        },
        {
          'offset_day_mode': TimeZone.OffsetDayMode.MONTH_WEEK_DAY,
          'month': 8,
          'week': 1,
          'day_in_week': 2,
          'from_month_end': True,
          'start_time_in_day': 30 * 60,
          'utc_offset': 1 * 3_600,
          'abbreviation': 'Test3',
        },
      )
    )
    
    def test_tz(tz_tuple, week_day, ordinal_date, is_dst, tm_gmtoff, abbr):
      tm_zone = abbr
      instant = TimeInstant.from_date_tuple_tz(tz, *tz_tuple[:6], 0, tz_tuple[6])
      struct_time_obj = struct_time((*tz_tuple[:6], week_day, ordinal_date, is_dst), {'tm_zone': tm_zone, 'tm_gmtoff': tm_gmtoff})
      struct_time_equals(
        instant.to_struct_time(tz),
        struct_time_obj
      )
      self.assertEqual(
        instant,
        TimeInstant.from_struct_time(struct_time_obj)
      )
      self.assertEqual(
        instant,
        TimeInstant(struct_time_obj)
      )
    
    test_tz((2016, 12, 31, 0,  59, 58, False), 5, 366, 0, 3600, 'Test3')
    test_tz((2016, 12, 31, 0,  59, 59, False), 5, 366, 0, 3600, 'Test3')
    test_tz((2016, 12, 31, 1,  0,  0,  False), 5, 366, 0, 3600, 'Test3')
    test_tz((2016, 12, 31, 23, 59, 58, False), 5, 366, 0, 3600, 'Test3')
    test_tz((2016, 12, 31, 23, 59, 59, False), 5, 366, 0, 3600, 'Test3')
    test_tz((2017, 1,  1,  0,  0,  0,  False), 6, 1,   0, 3600, 'Test1')
    test_tz((2017, 1,  1,  0,  59, 58, False), 6, 1,   0, 3600, 'Test1')
    test_tz((2017, 1,  1,  0,  59, 59, False), 6, 1,   0, 3600, 'Test1')
    test_tz((2017, 1,  1,  0,  59, 60, False), 6, 1,   0, 3600, 'Test1')
    test_tz((2017, 1,  1,  1,  0,  0,  False), 6, 1,   0, 3600, 'Test1')
    test_tz((2017, 1,  1,  1,  0,  1,  False), 6, 1,   0, 3600, 'Test1')
    
    test_tz((2024, 4,  15, 4,  59, 59, False), 0, 106, 0, 3600, 'Test1')
    test_tz((2024, 4,  15, 6,  0,  0,  False), 0, 106, 1, 7200, 'Test2')
    
    test_tz((2024, 8,  26, 23, 29, 59, False), 0, 239, 1, 7200, 'Test2')
    test_tz((2024, 8,  26, 23, 30, 0,  False), 0, 239, 1, 7200, 'Test2')
    test_tz((2024, 8,  27, 0,  29, 59, False), 1, 240, 1, 7200, 'Test2')
    test_tz((2024, 8,  26, 23, 30, 0,  True ), 0, 239, 0, 3600, 'Test3')
    test_tz((2024, 8,  27, 0,  29, 59, True ), 1, 240, 0, 3600, 'Test3')
    test_tz((2024, 8,  27, 0,  30, 0,  False), 1, 240, 0, 3600, 'Test3')
  
  def test_monotonic_time_scale_tai(self):
    self.assertEqual(TimeInstant(3).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TAI), 3)
    self.assertEqual(TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TAI, 3).time, 3)
    self.assertEqual(
      TimeInstant.from_date_tuple_tai(2024, 4, 28, 12, 0, 0, 0).to_date_tuple_mono(TimeInstant.TIME_SCALES.TAI),
      (2024, 4, 28, 12, 0, 0, 0)
    )
    self.assertEqual(
      TimeInstant.from_date_tuple_mono(TimeInstant.TIME_SCALES.TAI, 2024, 4, 28, 12, 0, 0, 0).to_date_tuple_tai(),
      (2024, 4, 28, 12, 0, 0, 0)
    )
  
  def test_monotonic_time_scale_tt(self):
    self.assertEqual(TimeInstant(3).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TT), 3 + FixedPrec('32.184'))
    self.assertEqual(TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TT, 3).time, 3 - FixedPrec('32.184'))
    self.assertEqual(
      TimeInstant.from_date_tuple_tai(2024, 4, 28, 12, 0, 0, 0).to_date_tuple_mono(TimeInstant.TIME_SCALES.TT),
      (2024, 4, 28, 12, 0, 32, FixedPrec('0.184'))
    )
    self.assertEqual(
      TimeInstant.from_date_tuple_mono(TimeInstant.TIME_SCALES.TT, 2024, 4, 28, 12, 0, 32, FixedPrec('0.184')).to_date_tuple_tai(),
      (2024, 4, 28, 12, 0, 0, 0)
    )
  
  def test_monotonic_time_scale_tcg(self):
    def test(time_scale, tai_tuple, ts_tuple):
      self.assertEqual(
        TimeInstant.from_date_tuple_tai(*tai_tuple).to_date_tuple_mono(time_scale),
        ts_tuple
      )
      self.assertEqual(
        TimeInstant.from_date_tuple_mono(time_scale, *ts_tuple).to_date_tuple_tai(),
        tai_tuple
      )
    
    test(
      TimeInstant.TIME_SCALES.TCG,
      (1977, 1, 1, 0, 0, 0, 0),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.184'))
    )
    test(
      TimeInstant.TIME_SCALES.TCG,
      (1977, 1, 1, 0, 0, 0, FixedPrec('0.9999999993030709866')),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.184'))
    )
  
  def test_monotonic_time_scale_tcb(self):
    def test_approx(time_scale, tai_tuple, ts_tuple_start, ts_tuple_end):
      tcg_start = TimeInstant.from_date_tuple_mono(TimeInstant.TIME_SCALES.TCG, *ts_tuple_start).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      mono_secs = TimeInstant.from_date_tuple_tai(*tai_tuple).to_secs_since_epoch_mono(time_scale)
      tcg_end = TimeInstant.from_date_tuple_mono(TimeInstant.TIME_SCALES.TCG, *ts_tuple_end).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      self.assertTrue(
        tcg_start < mono_secs < tcg_end,
        f'{tcg_start} < {mono_secs} < {tcg_end}'
      )
      mono_start = TimeInstant.from_date_tuple_mono(time_scale, *ts_tuple_start).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      mono_end = TimeInstant.from_date_tuple_mono(time_scale, *ts_tuple_end).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      self.assertTrue(
        mono_start < tcg_start < mono_end,
        f'{mono_start} < {tcg_start} < {mono_end}'
      )
    
    test_approx(
      TimeInstant.TIME_SCALES.TCB,
      (1977, 1, 1, 0, 0, 0, 0),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.184')),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.185'))
    )
    test_approx(
      TimeInstant.TIME_SCALES.TCB,
      (1977, 1, 1, 0, 0, 1, 0),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.184')),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.185'))
    )
  
  def test_monotonic_time_scale_tcb_cycle(self):
    def test_cycle(instant: TimeInstant, places = 12):
      mono_secs_since_epoch = instant.to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCB)
      from_mono_secs = TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCB, mono_secs_since_epoch)
      self.assertAlmostEqual(instant.time, from_mono_secs.time, places, f'{instant.to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCB)} {from_mono_secs.to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCB)}')
    
    med_instant = TimeInstant(FixedPrec(TimeInstant.from_date_tuple_tai(1977, 6, 1, 0, 0, 0, 0).time, max_prec = 19))
    far_instant_future = TimeInstant(FixedPrec(10 ** 50, max_prec = 19))
    far_instant_past = TimeInstant(FixedPrec(-10 ** 50, max_prec = 19))
    test_cycle(med_instant)
    test_cycle(far_instant_future, 3)
    test_cycle(far_instant_past, 3)
  
  def test_monotonic_time_scale_gal_and_uni(self):
    def test_approx(time_scale, tai_tuple, ts_tuple_start, ts_tuple_end):
      tcg_start = TimeInstant.from_date_tuple_mono(TimeInstant.TIME_SCALES.TCG, *ts_tuple_start).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      mono_secs = TimeInstant.from_date_tuple_tai(*tai_tuple).to_secs_since_epoch_mono(time_scale)
      tcg_end = TimeInstant.from_date_tuple_mono(TimeInstant.TIME_SCALES.TCG, *ts_tuple_end).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      self.assertTrue(
        tcg_start < mono_secs < tcg_end,
        f'{tcg_start} < {mono_secs} < {tcg_end}'
      )
      mono_start = TimeInstant.from_date_tuple_mono(time_scale, *ts_tuple_start).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      mono_end = TimeInstant.from_date_tuple_mono(time_scale, *ts_tuple_end).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.TCG)
      self.assertTrue(
        mono_start < tcg_start < mono_end,
        f'{mono_start} < {tcg_start} < {mono_end}'
      )
    
    test_approx(
      TimeInstant.TIME_SCALES.GALACTIC_COORDINATE_TIME,
      (1977, 1, 1, 0, 0, 0, 0),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.184')),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.185'))
    )
    test_approx(
      TimeInstant.TIME_SCALES.GALACTIC_COORDINATE_TIME,
      (1977, 1, 1, 0, 0, 1, 0),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.184')),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.185'))
    )
    
    test_approx(
      TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME,
      (1977, 1, 1, 0, 0, 0, 0),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.184')),
      (1977, 1, 1, 0, 0, 32, FixedPrec('0.185'))
    )
    test_approx(
      TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME,
      (1977, 1, 1, 0, 0, 1, 0),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.184')),
      (1977, 1, 1, 0, 0, 33, FixedPrec('0.185'))
    )
  
  def test_monotonic_time_scale_ut1(self):
    def test(tai_instant, ut1_instant):
      self.assertEqual(TimeInstant(tai_instant).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UT1), ut1_instant)
      self.assertEqual(TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UT1, ut1_instant).time, tai_instant)
    
    test(0, TimeInstant.UT1_TAI_OFFSETS[0].ut1_minus_tai)
    test(63643017636, 63643017636 + FixedPrec('-36.2859339'))
    test(63643060836, 63643060836 + FixedPrec('-36.28641715'))
    test(63643104036, 63643104036 + FixedPrec('-36.2869004'))
    future = TimeInstant.now().time + 2 * 365 * 86400
    test(future, future + TimeInstant.UT1_TAI_OFFSETS[-1].ut1_minus_tai)
  
  def test_solar_time_scales(self):
    longitude = 15
    
    def test(ut1_instant, solar_instant, true_solar):
      self.assertEqual(TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UT1, ut1_instant).to_secs_since_epoch_solar(longitude, true_solar), solar_instant)
      self.assertEqual(TimeInstant.from_secs_since_epoch_solar(longitude, true_solar, solar_instant).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UT1), ut1_instant)
    
    test(0, 3600, False)
    D = FixedPrec('6.24004077')
    test(0, 3600 + (FixedPrec('-7.659') * D.sin() + FixedPrec('9.863') * (2 * D + FixedPrec('3.5932')).sin()) * 60, True)
  
  def test_fixedprec_offset_to_str(self):
    def test(offset, offset_no_colon, offset_colon, offset_prec_0, offset_prec_1, offset_prec_2):
      offset = FixedPrec(offset)
      self.assertEqual(TimeInstant.fixedprec_offset_to_str(offset, minute_colon = False), offset_no_colon)
      self.assertEqual(TimeInstant.fixedprec_offset_to_str(offset, minute_colon = True), offset_colon)
      self.assertEqual(TimeInstant.fixedprec_offset_to_str(offset, precision = 0), offset_prec_0)
      self.assertEqual(TimeInstant.fixedprec_offset_to_str(offset, precision = 1), offset_prec_1)
      self.assertEqual(TimeInstant.fixedprec_offset_to_str(offset, precision = 2), offset_prec_2)
      self.assertEqual(TimeInstant.str_offset_to_fixedprec(offset_no_colon), offset)
      self.assertEqual(TimeInstant.str_offset_to_fixedprec(offset_colon), offset)
      self.assertEqual(TimeInstant.str_offset_to_fixedprec(offset_prec_0), trunc(offset))
      self.assertEqual(TimeInstant.str_offset_to_fixedprec(offset_prec_1), offset)
      self.assertEqual(TimeInstant.str_offset_to_fixedprec(offset_prec_2), offset)
    
    test(-3600,   '-0100'      , '-01:00'     , '-01:00:00', '-01:00:00.0', '-01:00:00.00')
    test(-61,     '-00:01:01'  , '-00:01:01'  , '-00:01:01', '-00:01:01.0', '-00:01:01.00')
    test(-60,     '-0001'      , '-00:01'     , '-00:01:00', '-00:01:00.0', '-00:01:00.00')
    test(-59,     '-00:00:59'  , '-00:00:59'  , '-00:00:59', '-00:00:59.0', '-00:00:59.00')
    test('-58.9', '-00:00:58.9', '-00:00:58.9', '-00:00:58', '-00:00:58.9', '-00:00:58.90')
    test(0,       'Z'          , '+00:00'     , '+00:00:00', '+00:00:00.0', '+00:00:00.00')
    test('58.9',  '+00:00:58.9', '+00:00:58.9', '+00:00:58', '+00:00:58.9', '+00:00:58.90')
    test(59,      '+00:00:59'  , '+00:00:59'  , '+00:00:59', '+00:00:59.0', '+00:00:59.00')
    test(60,      '+0001'      , '+00:01'     , '+00:01:00', '+00:01:00.0', '+00:01:00.00')
    test(61,      '+00:01:01'  , '+00:01:01'  , '+00:01:01', '+00:01:01.0', '+00:01:01.00')
    test(3600,    '+0100'      , '+01:00'     , '+01:00:00', '+01:00:00.0', '+01:00:00.00')
  
  def test_to_format_string_tai(self):
    time_instant = TimeInstant.from_date_tuple_tai(2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_tai('a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test G:%G u:%u V:%V :z:%:z .10f:%.10f .15f:%.15f .0z:%.0z .1z:%.1z .15z:%.15z'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:+00:00:37 Z:Time Atomic International %:% str:test G:2024 u:7 V:15 :z:+00:00:37 .10f:0567891300 .15f:056789130000000 .0z:+00:00:37 .1z:+00:00:37.0 .15z:+00:00:37.000000000000000'
    )
    time_instant_2 = TimeInstant.from_date_tuple_tai(2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_tai('U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_utc(self):
    time_instant = TimeInstant.from_date_tuple_utc(2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_utc('a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test G:%G u:%u V:%V :z:%:z .10f:%.10f .15f:%.15f .0z:%.0z .1z:%.1z .15z:%.15z'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:Z Z:Universal Time Coordinated %:% str:test G:2024 u:7 V:15 :z:+00:00 .10f:0567891300 .15f:056789130000000 .0z:+00:00:00 .1z:+00:00:00.0 .15z:+00:00:00.000000000000000'
    )
    time_instant_2 = TimeInstant.from_date_tuple_utc(2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_utc('U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_tz(self):
    tz = TimeZone(3_600)
    
    time_instant = TimeInstant.from_date_tuple_tz(tz, 2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_tz(tz, 'a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:+0100 Z:NULL %:% str:test'
    )
    time_instant_2 = TimeInstant.from_date_tuple_tz(tz, 2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_tz(tz, 'U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_mono(self):
    ts = TimeInstant.TIME_SCALES.TT
    
    time_instant = TimeInstant.from_date_tuple_mono(ts, 2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_mono(ts, 'a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:+00:01:09.184 Z:TT %:% str:test'
    )
    time_instant_2 = TimeInstant.from_date_tuple_mono(ts, 2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_mono(ts, 'U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_solar(self):
    longitude = 15
    true_solar = False
    
    time_instant = TimeInstant.from_date_tuple_solar(longitude, true_solar, 2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_solar(longitude, true_solar, 'a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test'),
      f'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:{TimeInstant.fixedprec_offset_to_str(time_instant.get_mono_tai_offset(TimeInstant.TIME_SCALES.UT1) + 3600 + 37)} Z:Mean Solar Time 15deg Longitude %:% str:test'
    )
    time_instant_2 = TimeInstant.from_date_tuple_solar(longitude, true_solar, 2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_solar(longitude, true_solar, 'U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_smear_utc(self):
    smear_plan = LeapSmearPlan(
      LeapSmearSingle(
        start_basis = LeapBasis.START,
        secs_before_start_basis = 5,
        end_basis = LeapBasis.END,
        secs_after_end_basis = 5,
        type = SmearType.LINEAR
      ),
      {}
    )
    
    time_instant = TimeInstant.from_date_tuple_smear_utc(smear_plan, 2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_smear_utc(smear_plan, 'a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:Z Z:Universal Time Coordinated (Smeared) %:% str:test'
    )
    time_instant_2 = TimeInstant.from_date_tuple_smear_utc(smear_plan, 2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_smear_utc(smear_plan, 'U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_to_format_string_smear_tz(self):
    smear_plan = LeapSmearPlan(
      LeapSmearSingle(
        start_basis = LeapBasis.START,
        secs_before_start_basis = 5,
        end_basis = LeapBasis.END,
        secs_after_end_basis = 5,
        type = SmearType.LINEAR
      ),
      {}
    )
    tz = TimeZone(3_600)
    
    time_instant = TimeInstant.from_date_tuple_smear_tz(smear_plan, tz, 2024, 4, 14, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant.to_format_string_smear_tz(smear_plan, tz, 'a:%a A:%A b:%b B:%B c:%c d:%d f:%f H:%H I:%I j:%j m:%m M:%M p:%p S:%S U:%U w:%w W:%W x:%x X:%X y:%y Y:%Y z:%z Z:%Z %%:%% str:test'),
      'a:Sun A:Sunday b:Apr B:April c:Sun Apr 14 13:02:03 2024 d:14 f:056789 H:13 I:01 j:105 m:04 M:02 p:PM S:03 U:15 w:0 W:15 x:04/14/24 X:13:02:03 y:24 Y:2024 z:+0100 Z:NULL (Smeared) %:% str:test'
    )
    time_instant_2 = TimeInstant.from_date_tuple_smear_tz(smear_plan, tz, 2024, 4, 15, 13, 2, 3, FixedPrec('0.05678913'))
    self.assertEqual(
      time_instant_2.to_format_string_smear_tz(smear_plan, tz, 'U:%U W:%W'),
      'U:15 W:16'
    )
  
  def test_from_format_string_tai(self):
    ...
  
  def test_from_format_string_utc(self):
    ...
  
  def test_from_format_string_tz(self):
    ...
  
  def test_from_format_string_mono(self):
    ...
  
  def test_from_format_string_solar(self):
    ...
  
  def test_from_format_string_smear_utc(self):
    ...
  
  def test_from_format_string_smear_tz(self):
    ...
  
  def test_from_format_string_generic(self):
    ...
  
  def test_from_format_string_smear_generic(self):
    ...
  
  def test_generated_timezones(self):
    chicago = TIMEZONES['proleptic_variable']['America/Chicago']
    sydney = TIMEZONES['proleptic_variable']['Australia/Sydney']
    
    def test(tz, date_tup, date_tup_tz, offset, is_dst):
      instant = TimeInstant.from_date_tuple_utc(*date_tup)
      self.assertEqual(instant.to_date_tuple_tz(tz), date_tup_tz)
      self.assertEqual(instant.get_current_tz_offset(tz)[0], offset)
      self.assertEqual(instant.to_struct_time(tz).tm_isdst, is_dst)
    
    test(chicago, (2024, 3,  10, 7,  59, 59, 0), (2024, 3,  10, 1, 59, 59, 0, False), -6 * 3600, 0)
    test(chicago, (2024, 3,  10, 8,  0,  0,  0), (2024, 3,  10, 3, 0,  0,  0, False), -5 * 3600, 1)
    test(chicago, (2024, 11, 3,  6,  59, 59, 0), (2024, 11, 3,  1, 59, 59, 0, False), -5 * 3600, 1)
    test(chicago, (2024, 11, 3,  7,  0,  0,  0), (2024, 11, 3,  1, 0,  0,  0, True ), -6 * 3600, 0)
    
    test(sydney,  (2024, 4,  6,  15, 59, 59, 0), (2024, 4,  7,  2, 59, 59, 0, False), 11 * 3600, 1)
    test(sydney,  (2024, 4,  6,  16, 0,  0,  0), (2024, 4,  7,  2, 0,  0,  0, True ), 10 * 3600, 0)
    test(sydney,  (2024, 10, 5,  15, 59, 59, 0), (2024, 10, 6,  1, 59, 59, 0, False), 10 * 3600, 0)
    test(sydney,  (2024, 10, 5,  16, 0,  0,  0), (2024, 10, 6,  3, 0,  0,  0, False), 11 * 3600, 1)
  
  def test_leap_smear_utc(self):
    with TimeInstant._temp_add_leap_sec(27, ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1))):
      smear_plan = LeapSmearPlan(
        LeapSmearSingle(
          start_basis = LeapBasis.START,
          secs_before_start_basis = 5,
          end_basis = LeapBasis.END,
          secs_after_end_basis = 5,
          type = SmearType.LINEAR
        ),
        {}
      )
      
      def six_digit_trunc(num):
        return trunc(num * 1_000_000) / 1_000_000
      
      def test(delta, utc_tuple, smear_utc_tuple, offset):
        instant = current_instant + TimeDelta(delta)
        utc_tuple = *utc_tuple[:6], FixedPrec(utc_tuple[6])
        smear_utc_tuple = *smear_utc_tuple[:6], FixedPrec(smear_utc_tuple[6])
        inst_from_utc = TimeInstant.from_date_tuple_utc(*utc_tuple)
        inst_from_utc_smear = TimeInstant.from_date_tuple_smear_utc(smear_plan, *smear_utc_tuple)
        self.assertAlmostEqual(instant.time, inst_from_utc.time, 5)
        self.assertAlmostEqual(instant.time, inst_from_utc_smear.time, 5)
        self.assertEqual(instant.to_date_tuple_utc(), utc_tuple)
        smear_utc_output = instant.to_date_tuple_smear_utc(smear_plan)
        self.assertEqual((*smear_utc_output[:6], six_digit_trunc(smear_utc_output[6])), smear_utc_tuple)
        smear_offset = instant.get_smear_utc_tai_offset(smear_plan)
        self.assertEqual(six_digit_trunc(smear_offset), FixedPrec(offset))
      
      current_instant = TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 54, FixedPrec('0.9'))
      
      test('0',    (2016, 12, 31, 23, 59, 54, '0.9'), (2016, 12, 31, 23, 59, 54, '0.9'     ), '-36'       )
      test('0.1',  (2016, 12, 31, 23, 59, 55, '0'  ), (2016, 12, 31, 23, 59, 55, '0'       ), '-36'       )
      test('1.1',  (2016, 12, 31, 23, 59, 56, '0'  ), (2016, 12, 31, 23, 59, 55, '0.909090'), '-36.090909')
      test('4.1',  (2016, 12, 31, 23, 59, 59, '0'  ), (2016, 12, 31, 23, 59, 58, '0.636363'), '-36.363636')
      test('5.1',  (2016, 12, 31, 23, 59, 60, '0'  ), (2016, 12, 31, 23, 59, 59, '0.545454'), '-36.454545')
      test('5.2',  (2016, 12, 31, 23, 59, 60, '0.1'), (2016, 12, 31, 23, 59, 59, '0.636363'), '-36.463636')
      test('6',    (2016, 12, 31, 23, 59, 60, '0.9'), (2017, 1,  1,  0,  0,  0,  '0.363636'), '-36.536363')
      test('6.1',  (2017, 1,  1,  0,  0,  0,  '0'  ), (2017, 1,  1,  0,  0,  0,  '0.454545'), '-36.545454')
      test('7.1',  (2017, 1,  1,  0,  0,  1,  '0'  ), (2017, 1,  1,  0,  0,  1,  '0.363636'), '-36.636363')
      test('10.1', (2017, 1,  1,  0,  0,  4,  '0'  ), (2017, 1,  1,  0,  0,  4,  '0.090909'), '-36.909090')
      test('11.1', (2017, 1,  1,  0,  0,  5,  '0'  ), (2017, 1,  1,  0,  0,  5,  '0'       ), '-37'       )
      test('11.2', (2017, 1,  1,  0,  0,  5,  '0.1'), (2017, 1,  1,  0,  0,  5,  '0.1'     ), '-37'       )
      
      current_instant = TimeInstant.from_date_tuple_utc(2017, 12, 31, 23, 59, 54, FixedPrec('0.9'))
      
      test('0',   (2017, 12, 31, 23, 59, 54, '0.9'), (2017, 12, 31, 23, 59, 54, '0.9'     ), '-37'       )
      test('0.1', (2017, 12, 31, 23, 59, 55, '0'  ), (2017, 12, 31, 23, 59, 55, '0'       ), '-37'       )
      test('1.1', (2017, 12, 31, 23, 59, 56, '0'  ), (2017, 12, 31, 23, 59, 56, '0.111111'), '-36.888888')
      test('3.1', (2017, 12, 31, 23, 59, 58, '0'  ), (2017, 12, 31, 23, 59, 58, '0.333333'), '-36.666666')
      test('4.1', (2018, 1,  1,  0,  0,  0,  '0'  ), (2017, 12, 31, 23, 59, 59, '0.444444'), '-36.555555')
      test('5.1', (2018, 1,  1,  0,  0,  1,  '0'  ), (2018, 1,  1,  0,  0,  0,  '0.555555'), '-36.444444')
      test('8.1', (2018, 1,  1,  0,  0,  4,  '0'  ), (2018, 1,  1,  0,  0,  3,  '0.888888'), '-36.111111')
      test('9.1', (2018, 1,  1,  0,  0,  5,  '0'  ), (2018, 1,  1,  0,  0,  5,  '0'       ), '-36'       )
      test('9.2', (2018, 1,  1,  0,  0,  5,  '0.1'), (2018, 1,  1,  0,  0,  5,  '0.1'     ), '-36'       )
