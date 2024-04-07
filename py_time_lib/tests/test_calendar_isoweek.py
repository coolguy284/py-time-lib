import unittest

from ..calendars.iso_weekdate import IsoWeekDate

class TestCalendarIsoWeek(unittest.TestCase):
  def test_instantiate(self):
    IsoWeekDate(0)
  
  def test_repr(self):
    self.assertEqual(repr(IsoWeekDate(2024, 2, 3)), 'IsoWeekDate(year = 2024, week = 2, day = 3)')
  
  def test_str(self):
    self.assertEqual(str(IsoWeekDate(2024, 2, 3)), '2024-W02-3')
