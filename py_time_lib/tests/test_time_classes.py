import unittest

from ..calendars.gregorian import GregorianDate
from ..data.leap_seconds import NOMINAL_SECS_PER_DAY
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
    self.assertEqual(str(TimeInstant(FixedPrec(1000)) + TimeDelta(FixedPrec('0.1'))), 'T+1000.1')
  
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
    second_last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 3]['start_instant']
    last_leap_start = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['start_instant']
    second_last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2]['utc_tai_delta']
    last_utc_offset = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index]['utc_tai_delta']
    last_leap_utc_secs = last_leap_start + last_utc_offset + 1
    second_last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 2]['leap_utc_delta']
    last_leap_delta = TimeInstant.TAI_TO_UTC_OFFSET_TABLE[last_leap_index - 1]['leap_utc_delta']
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
      
      leap_normal_pos_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2017, 1, 1).to_days_since_epoch() * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_normal_neg_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2018, 1, 1).to_days_since_epoch() * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_big_pos_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2018, 7, 1).to_days_since_epoch() * TimeInstant.NOMINAL_SECS_PER_DAY)
      leap_big_neg_midnight = TimeInstant.from_utc_secs_since_epoch(GregorianDate(2019, 1, 1).to_days_since_epoch() * TimeInstant.NOMINAL_SECS_PER_DAY)
      
      def test_instant(time_delta, tai_tuple, utc_tuple):
        instant = current_leap + TimeDelta(FixedPrec(time_delta))
        self.assertEqual(instant.to_gregorian_date_tuple_tai(), tai_tuple[:6] + (FixedPrec(tai_tuple[6]),))
        self.assertEqual(instant.to_gregorian_date_tuple_utc(), utc_tuple[:6] + (FixedPrec(utc_tuple[6]),))
      
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
    self.assertEqual(TimeInstant.from_gregorian_date_tuple_tai(*tai_tuple).to_gregorian_date_tuple_tai(), tai_tuple)
  
  def test_from_utc_tuple(self):
    with TimeInstant._temp_add_leap_secs(27, [
        ('2017-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(1)),
        ('2018-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-2)),
        ('2018-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(2)),
      ]):
      
      def test(*date_tuple):
        date_tuple = *date_tuple[:6], FixedPrec(date_tuple[6])
        instant = TimeInstant.from_gregorian_date_tuple_utc(*date_tuple)
        self.assertEqual(date_tuple, instant.to_gregorian_date_tuple_utc())
      
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
