from datetime import date as datetime_date
from unittest import TestCase

from ... import DateDelta, GregorianDate, IsoWeekDate

class TestCalendarDateBase(TestCase):
  def test_date_delta_str(self):
    self.assertEqual(str(DateDelta(1000)), '1000 days')
    self.assertEqual(str(DateDelta(-1000)), '-1000 days')
    self.assertEqual(str(DateDelta(0)), '0 days')
  
  def test_date_delta_repr(self):
    self.assertEqual(repr(DateDelta(1000)), 'DateDelta(1000)')
    self.assertEqual(repr(DateDelta(-1000)), 'DateDelta(-1000)')
    self.assertEqual(repr(DateDelta(0)), 'DateDelta(0)')
  
  def test_date_delta_basic_ops(self):
    self.assertEqual(str(-DateDelta(1)), '-1 days')
    self.assertEqual(str(-DateDelta(0)), '0 days')
    self.assertEqual(str(+DateDelta(1)), '1 days')
    self.assertEqual(str(+DateDelta(0)), '0 days')
    self.assertEqual(str(abs(DateDelta(1))), '1 days')
    self.assertEqual(str(abs(DateDelta(0))), '0 days')
    self.assertEqual(str(abs(DateDelta(-1))), '1 days')
    self.assertEqual(str(DateDelta(3) + DateDelta(2)), '5 days')
    self.assertEqual(str(DateDelta(3) - DateDelta(2)), '1 days')
    self.assertEqual(str(DateDelta(3) * 4), '12 days')
    self.assertEqual(DateDelta(3) // 3, DateDelta(1))
    self.assertEqual(DateDelta(3) / DateDelta(2), 1.5)
    self.assertEqual(DateDelta(14) // DateDelta(3), 4)
    self.assertEqual(DateDelta(14) % DateDelta(3), DateDelta(2))
    self.assertEqual(divmod(DateDelta(14), DateDelta(3)), (4, DateDelta(2)))
    
    self.assertEqual(str(4 * DateDelta(3)), '12 days')
    with self.assertRaises(TypeError):
      self.assertEqual(3 // DateDelta(3), DateDelta(1))
  
  def test_date_base_basic_ops(self):
    self.assertEqual((GregorianDate(1000) + DateDelta(3)).days_since_epoch, 1003)
    self.assertEqual((GregorianDate(1000) - DateDelta(3)).days_since_epoch, 997)
    self.assertEqual(str(GregorianDate(1000) - GregorianDate(993)), '7 days')
    
    self.assertEqual((DateDelta(3) + GregorianDate(1000)).days_since_epoch, 1003)
  
  def test_date_delta_relational_ops(self):
    self.assertEqual(DateDelta(1) > DateDelta(0), True)
    self.assertEqual(DateDelta(1) < DateDelta(0), False)
    self.assertEqual(DateDelta(1) >= DateDelta(0), True)
    self.assertEqual(DateDelta(1) <= DateDelta(0), False)
    self.assertEqual(DateDelta(1) == DateDelta(0), False)
    self.assertEqual(DateDelta(1) != DateDelta(0), True)
    self.assertEqual(DateDelta(1) > DateDelta(1), False)
    self.assertEqual(DateDelta(1) < DateDelta(1), False)
    self.assertEqual(DateDelta(1) >= DateDelta(1), True)
    self.assertEqual(DateDelta(1) <= DateDelta(1), True)
    self.assertEqual(DateDelta(1) == DateDelta(1), True)
    self.assertEqual(DateDelta(1) != DateDelta(1), False)
    self.assertEqual(DateDelta(1) > DateDelta(2), False)
    self.assertEqual(DateDelta(1) < DateDelta(2), True)
    self.assertEqual(DateDelta(1) >= DateDelta(2), False)
    self.assertEqual(DateDelta(1) <= DateDelta(2), True)
    self.assertEqual(DateDelta(1) == DateDelta(2), False)
    self.assertEqual(DateDelta(1) != DateDelta(2), True)
    self.assertEqual(DateDelta(1) == None, False)
    self.assertEqual(DateDelta(1) != None, True)
  
  def test_date_base_relational_ops(self):
    self.assertEqual(GregorianDate(1) > GregorianDate(0), True)
    self.assertEqual(GregorianDate(1) < GregorianDate(0), False)
    self.assertEqual(GregorianDate(1) >= GregorianDate(0), True)
    self.assertEqual(GregorianDate(1) <= GregorianDate(0), False)
    self.assertEqual(GregorianDate(1) == GregorianDate(0), False)
    self.assertEqual(GregorianDate(1) != GregorianDate(0), True)
    self.assertEqual(GregorianDate(1) > GregorianDate(1), False)
    self.assertEqual(GregorianDate(1) < GregorianDate(1), False)
    self.assertEqual(GregorianDate(1) >= GregorianDate(1), True)
    self.assertEqual(GregorianDate(1) <= GregorianDate(1), True)
    self.assertEqual(GregorianDate(1) == GregorianDate(1), True)
    self.assertEqual(GregorianDate(1) != GregorianDate(1), False)
    self.assertEqual(GregorianDate(1) > GregorianDate(2), False)
    self.assertEqual(GregorianDate(1) < GregorianDate(2), True)
    self.assertEqual(GregorianDate(1) >= GregorianDate(2), False)
    self.assertEqual(GregorianDate(1) <= GregorianDate(2), True)
    self.assertEqual(GregorianDate(1) == GregorianDate(2), False)
    self.assertEqual(GregorianDate(1) != GregorianDate(2), True)
    self.assertEqual(GregorianDate(1) == None, False)
    self.assertEqual(GregorianDate(1) != None, True)
  
  def test_hash_datedelta(self):
    self.assertEqual(hash(DateDelta(3)), hash(('DateDelta', 3)))
  
  def test_hash_datebase(self):
    self.assertEqual(hash(GregorianDate(3)), hash(('DateBase', 3)))
  
  def test_from_to_date(self):
    def test(date_tup):
      datetime_date_obj = datetime_date(*date_tup)
      greg_date = GregorianDate(*date_tup)
      iso_date = IsoWeekDate(greg_date)
      self.assertEqual(greg_date.to_datetime_date(), datetime_date_obj)
      self.assertEqual(GregorianDate.from_datetime_date(datetime_date_obj), greg_date)
      self.assertEqual(GregorianDate(datetime_date_obj), greg_date)
      self.assertEqual(iso_date.to_datetime_date(), datetime_date_obj)
      self.assertEqual(IsoWeekDate.from_datetime_date(datetime_date_obj), iso_date)
      self.assertEqual(IsoWeekDate(datetime_date_obj), iso_date)
    
    test((2024, 4, 24))
    test((2100, 2, 28))
