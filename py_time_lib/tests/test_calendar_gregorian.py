import unittest

from ..calendars.gregorian import days_in_year, is_leap

class TestCalendarGregorian(unittest.TestCase):
  def test_leap_year_2020(self):
    self.assertEqual(is_leap(2020), True)
  
  def test_leap_year_2021(self):
    self.assertEqual(is_leap(2021), False)
  
  def test_leap_year_1900(self):
    self.assertEqual(is_leap(1900), False)
  
  def test_leap_year_2000(self):
    self.assertEqual(is_leap(2000), True)
  
  def test_year_2000_days(self):
    self.assertEqual(days_in_year(2000), 366)
  
  def test_year_2001_days(self):
    self.assertEqual(days_in_year(2001), 365)
  
  def test_year_1900_days(self):
    self.assertEqual(days_in_year(1900), 365)
