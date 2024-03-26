import random, unittest

from ..calendars.julian import date_to_days_since_epoch, days_in_month, days_in_year, days_since_epoch_to_date, is_leap, JulianDate

class TestCalendarJulian(unittest.TestCase):
  def test_leap_year_2020(self):
    self.assertEqual(is_leap(2020), True)
  
  def test_leap_year_2021(self):
    self.assertEqual(is_leap(2021), False)
  
  def test_leap_year_1900(self):
    self.assertEqual(is_leap(1900), True)
  
  def test_leap_year_2000(self):
    self.assertEqual(is_leap(2000), True)
  
  def test_year_2000_days(self):
    self.assertEqual(days_in_year(2000), 366)
  
  def test_year_2001_days(self):
    self.assertEqual(days_in_year(2001), 365)
  
  def test_year_1900_days(self):
    self.assertEqual(days_in_year(1900), 366)
  
  def test_class_repr(self):
    jd = JulianDate(2024, 1, 1)
    self.assertEqual(repr(jd), 'JulianDate(2024, 1, 1)')
  
  def test_class_str(self):
    jd = JulianDate(2024, 1, 1)
    self.assertEqual(str(jd), '2024-01-01')
  
  def test_month_days_2024_02(self):
    self.assertEqual(days_in_month(2024, 2), 29)
  
  def test_month_days_2023_02(self):
    self.assertEqual(days_in_month(2023, 2), 28)
  
  def test_feb_29_2024(self):
    _ = JulianDate(2024, 2, 29)
  
  def test_feb_29_2023(self):
    with self.assertRaises(Exception):
      _ = JulianDate(2023, 2, 29)
  
  def test_date_to_days_since_epoch(self):
    test = lambda year: self.assertEqual(days_in_year(year), date_to_days_since_epoch(year + 1, 1, 1) - date_to_days_since_epoch(year, 1, 1))
    
    #test(-20000)
    #test(-19999)
    #test(-19998)
    #test(-19997)
    #test(-19996)
    #test(-19995)
    #test(-19994)
    #test(-19993)
    #test(2020)
    #test(2021)
    #test(1900)
    #test(1901)
    
    random.seed(42)
    
    for _ in range(1000):
      test(random.randint(-1000000, 1000000))
  
  def test_days_since_epoch_to_date(self):
    random.seed(42)
    
    for _ in range(1000):
      days = random.randint(-1000000000000, 1000000000000)
      self.assertEqual(days, date_to_days_since_epoch(*days_since_epoch_to_date(days)))
