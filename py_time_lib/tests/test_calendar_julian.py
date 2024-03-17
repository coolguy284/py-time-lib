import unittest

from ..calendars.julian import is_leap

class TestCalendarJulian(unittest.TestCase):
  def test_leap_year_2020(self):
    self.assertEqual(is_leap(2020), True)
  
  def test_leap_year_2021(self):
    self.assertEqual(is_leap(2021), False)
  
  def test_leap_year_1900(self):
    self.assertEqual(is_leap(1900), False)
  
  def test_leap_year_2000(self):
    self.assertEqual(is_leap(2000), True)
