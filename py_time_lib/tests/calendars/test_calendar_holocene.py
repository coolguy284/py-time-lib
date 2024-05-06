from unittest import TestCase

from ... import GregorianDate, HoloceneDate

class TestCalendarHolocene(TestCase):
  def test_basic_creation(self):
    self.assertEqual(HoloceneDate(GregorianDate(2024, 4, 7)).to_date_tuple(), (12024, 4, 7))
  
  def test_repr(self):
    self.assertEqual(repr(HoloceneDate(12024, 2, 3)), 'HoloceneDate(year = 12024, month = 2, day = 3)')
  
  def test_str(self):
    self.assertEqual(str(HoloceneDate(12024, 2, 3)), '12024-02-03')
  
  def test_no_attributes(self):
    with self.assertRaises(AttributeError):
      d1 = HoloceneDate(2024, 3, 26)
      d1.prop = False
