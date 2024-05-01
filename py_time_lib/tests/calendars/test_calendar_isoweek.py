import unittest

from ... import IsoWeekDate

class TestCalendarIsoWeek(unittest.TestCase):
  def test_instantiate(self):
    IsoWeekDate(0)
  
  def test_repr(self):
    self.assertEqual(repr(IsoWeekDate(2024, 2, 3)), 'IsoWeekDate(year = 2024, week = 2, day = 3)')
  
  def test_str(self):
    self.assertEqual(str(IsoWeekDate(2024, 2, 3)), '2024-W02-3')
  
  def test_construct_from_kwargs(self):
    self.assertEqual(str(IsoWeekDate(year = 2024, week = 4, day = 4)), '2024-W04-4')
  
  def test_no_attributes(self):
    with self.assertRaises(AttributeError):
      d1 = IsoWeekDate(2024, 8, 4)
      d1.prop = False
