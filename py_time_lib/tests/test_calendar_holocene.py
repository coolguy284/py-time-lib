import unittest

from ..calendars.holocene import HoloceneDate
from ..calendars.gregorian import GregorianDate

class TestCalendarHolocene(unittest.TestCase):
  def test_basic_creation(self):
    self.assertEqual(HoloceneDate(GregorianDate(2024, 4, 7)).to_date_tuple(), (12024, 4, 7))
