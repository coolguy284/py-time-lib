from datetime import date as datetime_date
from random import randint, seed
from unittest import TestCase

from ... import GregorianDate

cls = GregorianDate

class TestCalendarGregorian(TestCase):
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
    date = cls(2024, 1, 1)
    self.assertEqual(repr(date), 'GregorianDate(year = 2024, month = 1, day = 1)')
  
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
  
  def test_from_days_since_epoch_implicit(self):
    self.assertEqual(str(cls(1)), '0-01-02')
    self.assertEqual(str(cls(0)), '0-01-01')
    self.assertEqual(str(cls(-1)), '-1-12-31')
  
  def test_construct_from_date(self):
    self.assertEqual(str(cls(cls(1))), '0-01-02')
    self.assertEqual(str(cls(cls(0))), '0-01-01')
    self.assertEqual(str(cls(cls(-1))), '-1-12-31')
  
  # gregorian only tests
  
  def test_construct_from_kwargs(self):
    self.assertEqual(str(cls(year = 2024, month = 4, day = 30)), '2024-04-30')
  
  def test_add_days(self):
    self.assertEqual(str(cls('2024-04-02').add_days(1)), '2024-04-03')
  
  def test_day_of_week(self):
    # generated with datetime library
    self.assertEqual(cls('2000-01-01').day_of_week(), 6) # saturday
    self.assertEqual(cls('2024-04-04').day_of_week(), 4) # thursday
  
  def test_iso_week_tuple(self):
    # generated with datetime library
    self.assertEqual(cls('2000-01-01').to_iso_week_tuple(), (1999, 52, 6))
    self.assertEqual(cls('2024-04-04').to_iso_week_tuple(), (2024, 14, 4))
    self.assertEqual(cls('2024-12-31').to_iso_week_tuple(), (2025, 1, 2))
  
  def test_iso_week_full(self):
    start_day = GregorianDate.date_to_days_since_epoch(2019, 12, 20)
    
    def test(day_since_epoch):
      year, month, day = cls.days_since_epoch_to_date(day_since_epoch)
      date = cls(year, month, day)
      datetime_date_obj = datetime_date(year, month, day)
      self.assertEqual(date.iso_day_of_week(), datetime_date_obj.isoweekday())
      self.assertEqual(date.to_iso_week_tuple(), datetime_date_obj.isocalendar())
    
    for day_since_epoch in range(start_day, start_day + 366 * 7):
      test(day_since_epoch)
  
  def test_day_of_week_and_iso_week(self):
    monday = cls.from_iso_week_tuple(2024, 10, 1)
    saturday = cls.from_iso_week_tuple(2024, 10, 6)
    sunday = cls.from_iso_week_tuple(2024, 10, 7)
    self.assertEqual(monday.day_of_week(), 1)
    self.assertEqual(monday.iso_day_of_week(), 1)
    self.assertEqual(saturday.day_of_week(), 6)
    self.assertEqual(saturday.iso_day_of_week(), 6)
    self.assertEqual(sunday.day_of_week(), 0)
    self.assertEqual(sunday.iso_day_of_week(), 7)
  
  def test_from_unnormalized(self):
    date = cls.from_unnormalized(2024, 1, 32)
    self.assertEqual(date.to_date_tuple(), (2024, 2, 1))
    date = cls.from_unnormalized(2024, 1, 0)
    self.assertEqual(date.to_date_tuple(), (2023, 12, 31))
  
  def test_from_to_month_week_day(self):
    self.assertEqual(cls(2024, 1, 1).to_month_week_day(), (2024, 1, 1, 1))
    self.assertEqual(cls(2024, 1, 7).to_month_week_day(), (2024, 1, 1, 0))
    self.assertEqual(cls(2024, 4, 14).to_month_week_day(), (2024, 4, 2, 0))
    self.assertEqual(cls(2024, 4, 15).to_month_week_day(), (2024, 4, 3, 1))
    self.assertEqual(cls.from_month_week_day(2024, 1, 1, 1).to_date_tuple(), (2024, 1, 1))
    self.assertEqual(cls.from_month_week_day(2024, 1, 1, 0).to_date_tuple(), (2024, 1, 7))
    self.assertEqual(cls.from_month_week_day(2024, 4, 2, 0).to_date_tuple(), (2024, 4, 14))
    self.assertEqual(cls.from_month_week_day(2024, 4, 3, 1).to_date_tuple(), (2024, 4, 15))
  
  def test_from_to_month_week_day_month_end(self):
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 0), 4)
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 1), 5)
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 2), 5)
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 3), 4)
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 4), 4)
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 5), 4)
    self.assertEqual(cls.num_weeks_on_day(2024, 4, 6), 4)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 0), 5)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 1), 4)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 2), 4)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 3), 4)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 4), 4)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 5), 5)
    self.assertEqual(cls.num_weeks_on_day(2023, 12, 6), 5)
    self.assertEqual(cls(2024, 1, 1).to_month_week_day(from_month_end = True), (2024, 1, 5, 1))
    self.assertEqual(cls(2024, 1, 7).to_month_week_day(from_month_end = True), (2024, 1, 4, 0))
    self.assertEqual(cls(2024, 4, 14).to_month_week_day(from_month_end = True), (2024, 4, 3, 0))
    self.assertEqual(cls(2024, 4, 15).to_month_week_day(from_month_end = True), (2024, 4, 3, 1))
    self.assertEqual(cls(2024, 4, 28).to_month_week_day(from_month_end = True), (2024, 4, 1, 0))
    self.assertEqual(cls.from_month_week_day(2024, 1, 5, 1, from_month_end = True).to_date_tuple(), (2024, 1, 1))
    self.assertEqual(cls.from_month_week_day(2024, 1, 4, 0, from_month_end = True).to_date_tuple(), (2024, 1, 7))
    self.assertEqual(cls.from_month_week_day(2024, 4, 3, 0, from_month_end = True).to_date_tuple(), (2024, 4, 14))
    self.assertEqual(cls.from_month_week_day(2024, 4, 3, 1, from_month_end = True).to_date_tuple(), (2024, 4, 15))
    self.assertEqual(cls.from_month_week_day(2024, 4, 1, 0, from_month_end = True).to_date_tuple(), (2024, 4, 28))
  
  def test_month_day_week_comp_day(self):
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 25, 0, False), cls(2024, 4, 21))
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 25, 0, True), cls(2024, 4, 28))
    
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 30, 1, False), cls(2024, 4, 29))
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 30, 1, True), cls(2024, 5, 6))
    
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 25, 0, False, out_of_month_bounds_allowed = False), cls(2024, 4, 21))
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 25, 0, True, out_of_month_bounds_allowed = False), cls(2024, 4, 28))
    
    self.assertEqual(cls.from_month_day_of_week_comp_day(2024, 4, 30, 1, False, out_of_month_bounds_allowed = False), cls(2024, 4, 29))
    with self.assertRaises(ValueError):
      cls.from_month_day_of_week_comp_day(2024, 4, 30, 1, True, out_of_month_bounds_allowed = False)
