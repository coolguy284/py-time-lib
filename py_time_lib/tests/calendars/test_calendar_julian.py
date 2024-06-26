from random import randint, seed
from unittest import TestCase

from ... import JulianDate

cls = JulianDate

class TestCalendarJulian(TestCase):
  def test_leap_year_2020(self):
    self.assertEqual(cls.is_leap(2020), True)
  
  def test_leap_year_2021(self):
    self.assertEqual(cls.is_leap(2021), False)
  
  def test_leap_year_1900(self):
    self.assertEqual(cls.is_leap(1900), True)
  
  def test_leap_year_2000(self):
    self.assertEqual(cls.is_leap(2000), True)
  
  def test_year_2000_days(self):
    self.assertEqual(cls.days_in_year(2000), 366)
  
  def test_year_2001_days(self):
    self.assertEqual(cls.days_in_year(2001), 365)
  
  def test_year_1900_days(self):
    self.assertEqual(cls.days_in_year(1900), 366)
  
  def test_class_repr(self):
    date = cls(2024, 1, 1)
    self.assertEqual(repr(date), 'JulianDate(year = 2024, month = 1, day = 1)')
  
  def test_class_str(self):
    self.assertEqual(str(cls(2024, 1, 1)), '2024-01-01')
    self.assertEqual(str(cls(0, 1, 1)), '0-01-01')
    self.assertEqual(str(cls(-2024, 1, 1)), '-2024-01-01')
  
  def test_month_days_2024_02(self):
    self.assertEqual(cls.days_in_month(2024, 2), 29)
  
  def test_month_days_2023_02(self):
    self.assertEqual(cls.days_in_month(2023, 2), 28)
  
  def test_feb_29_2024(self):
    _ = cls(2024, 2, 29)
  
  def test_feb_29_2023(self):
    with self.assertRaises(ValueError):
      _ = cls(2023, 2, 29)
  
  def test_date_to_days_since_epoch(self):
    seed(42)
    
    for _ in range(1000):
      year = randint(-1000000, 1000000)
      self.assertEqual(cls.days_in_year(year), cls.date_to_days_since_epoch(year + 1, 1, 1) - cls.date_to_days_since_epoch(year, 1, 1))
  
  def test_days_since_epoch_to_date(self):
    seed(42)
    
    for _ in range(1000):
      days = randint(-1000000000000, 1000000000000)
      self.assertEqual(days, cls.date_to_days_since_epoch(*cls.days_since_epoch_to_date(days)), f'{days}, {cls.days_since_epoch_to_date(days)}')
  
  def test_date_to_days_overflow(self):
    self.assertEqual(cls.date_to_days_since_epoch(0, 13, 1), cls.date_to_days_since_epoch(1, 1, 1))
    self.assertEqual(cls.date_to_days_since_epoch(0, 25, 1), cls.date_to_days_since_epoch(2, 1, 1))
    self.assertEqual(cls.date_to_days_since_epoch(0, 788 * 12 + 1, 1), cls.date_to_days_since_epoch(788, 1, 1))
  
  def test_no_attributes(self):
    with self.assertRaises(AttributeError):
      d1 = cls(2024, 3, 26)
      d1.prop = False
  
  def test_from_iso_string(self):
    self.assertEqual(str(cls.from_iso_string('2024-04-02')), '2024-04-02')
    self.assertEqual(str(cls.from_iso_string('0-04-02')), '0-04-02')
    self.assertEqual(str(cls.from_iso_string('-2024-04-02')), '-2024-04-02')
  
  def test_from_iso_string_implicit(self):
    self.assertEqual(str(cls('2024-04-02')), '2024-04-02')
    self.assertEqual(str(cls('0-04-02')), '0-04-02')
    self.assertEqual(str(cls('-2024-04-02')), '-2024-04-02')
