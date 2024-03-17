import unittest

from ..calendars.gregorian import is_leap

class TestCalendarGregorian(unittest.TestCase):
  def test_leap_year_2020(self):
    self.assertEqual(is_leap(2020), True)
  
  def test_leap_year_2021(self):
    self.assertEqual(is_leap(2021), False)
  
  def test_leap_year_1900(self):
    self.assertEqual(is_leap(1900), True)
  
  def test_leap_year_2000(self):
    self.assertEqual(is_leap(2000), True)
