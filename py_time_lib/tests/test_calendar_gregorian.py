import random, unittest

from ..calendars.gregorian import GregorianDate

cls = GregorianDate

class TestCalendarGregorian(unittest.TestCase):
  def test_leap_year_2020(self):
    self.assertEqual(cls.is_leap(2020), True)
  
  def test_leap_year_2021(self):
    self.assertEqual(cls.is_leap(2021), False)
  
  def test_leap_year_1900(self):
    self.assertEqual(cls.is_leap(1900), False)
  
  def test_leap_year_2000(self):
    self.assertEqual(cls.is_leap(2000), True)
  
  def test_year_2000_days(self):
    self.assertEqual(cls.days_in_year(2000), 366)
  
  def test_year_2001_days(self):
    self.assertEqual(cls.days_in_year(2001), 365)
  
  def test_year_1900_days(self):
    self.assertEqual(cls.days_in_year(1900), 365)
  
  def test_class_repr(self):
    jd = GregorianDate(2024, 1, 1)
    self.assertEqual(repr(jd), 'GregorianDate(2024, 1, 1)')
  
  def test_class_str(self):
    self.assertEqual(str(cls(2024, 1, 1)), '2024-01-01')
    self.assertEqual(str(cls(0, 1, 1)), '0-01-01')
    self.assertEqual(str(cls(-2024, 1, 1)), '-2024-01-01')
  
  def test_month_days_2024_02(self):
    self.assertEqual(cls.days_in_month(2024, 2), 29)
  
  def test_month_days_2023_02(self):
    self.assertEqual(cls.days_in_month(2023, 2), 28)
  
  def test_feb_29_2024(self):
    _ = GregorianDate(2024, 2, 29)
  
  def test_feb_29_2023(self):
    with self.assertRaises(Exception):
      _ = GregorianDate(2023, 2, 29)
  
  def test_date_to_days_since_epoch(self):
    random.seed(42)
    
    for _ in range(1000):
      year = random.randint(-1000000, 1000000)
      self.assertEqual(cls.days_in_year(year), cls.date_to_days_since_epoch(year + 1, 1, 1) - cls.date_to_days_since_epoch(year, 1, 1))
  
  def test_days_since_epoch_to_date(self):
    random.seed(42)
    
    for _ in range(1000):
      days = random.randint(-1000000000000, 1000000000000)
      self.assertEqual(days, cls.date_to_days_since_epoch(*cls.days_since_epoch_to_date(days)), f'{days}, {cls.days_since_epoch_to_date(days)}')
  
  def test_date_to_days_overflow(self):
    self.assertEqual(cls.date_to_days_since_epoch(0, 13, 1), cls.date_to_days_since_epoch(1, 1, 1))
    self.assertEqual(cls.date_to_days_since_epoch(0, 25, 1), cls.date_to_days_since_epoch(2, 1, 1))
    self.assertEqual(cls.date_to_days_since_epoch(0, 788 * 12 + 1, 1), cls.date_to_days_since_epoch(788, 1, 1))
  
  def test_julian_day_diff(self):
    # https://en.wikipedia.org/wiki/Gregorian_calendar#Difference_between_Gregorian_and_Julian_calendar_dates
    self.assertEqual(cls(1700, 2, 28).days_diff_from_julian(), 10)
    self.assertEqual(cls(1700, 3, 1).days_diff_from_julian(), 11)
    self.assertEqual(cls(1800, 2, 28).days_diff_from_julian(), 11)
    self.assertEqual(cls(1800, 3, 1).days_diff_from_julian(), 12)
    self.assertEqual(cls(1900, 2, 28).days_diff_from_julian(), 12)
    self.assertEqual(cls(1900, 3, 1).days_diff_from_julian(), 13)
    self.assertEqual(cls(2100, 2, 28).days_diff_from_julian(), 13)
    self.assertEqual(cls(2100, 3, 1).days_diff_from_julian(), 14)
    self.assertEqual(cls(2200, 2, 28).days_diff_from_julian(), 14)
  
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
  
  # gregorian only tests
  
  def test_add_days(self):
    self.assertEqual(str(cls('2024-04-02').add_days(1)), '2024-04-03')
