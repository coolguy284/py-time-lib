import unittest

from ..calendars.holocene import HoloceneDate
from ..calendars.gregorian import GregorianDate

class TestCalendarHolocene(unittest.TestCase):
  def test_basic_creation(self):
    self.assertEqual(HoloceneDate(GregorianDate(2024, 4, 7)).to_date_tuple(), (12024, 4, 7))
  
  def test_repr(self):
    self.assertEqual(repr(HoloceneDate(12024, 2, 3)), 'HoloceneDate(year = 12024, month = 2, day = 3)')
  
  def test_str(self):
    self.assertEqual(str(HoloceneDate(12024, 2, 3)), '12024-02-03')
