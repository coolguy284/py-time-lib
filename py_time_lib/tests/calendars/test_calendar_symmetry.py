import unittest

from ...calendars.gregorian import GregorianDate
from ...calendars.symmetry import Symmetry010, Symmetry010LeapMonth, Symmetry454, Symmetry454LeapMonth

class TestCalendarSymmetry(unittest.TestCase):
  def test_epoch(self):
    epoch = GregorianDate(1, 1, 1)
    self.assertEqual(epoch.day_of_week(), 1)
    self.assertEqual(Symmetry010(epoch).to_date_tuple(), (1, 1, 1))
    self.assertEqual(Symmetry010LeapMonth(epoch).to_date_tuple(), (1, 1, 1))
    self.assertEqual(Symmetry454(epoch).to_date_tuple(), (1, 1, 1))
    self.assertEqual(Symmetry454LeapMonth(epoch).to_date_tuple(), (1, 1, 1))
  
  def leap_week(self):
    def test(gregorian, sym010, sym010l, sym454, sym454l):
      greg_instant = GregorianDate(*gregorian)
      
      self.assertEqual(Symmetry010(greg_instant).to_date_tuple(), sym010)
      self.assertEqual(Symmetry010LeapMonth(greg_instant).to_date_tuple(), sym010l)
      self.assertEqual(Symmetry454(greg_instant).to_date_tuple(), sym454)
      self.assertEqual(Symmetry454LeapMonth(greg_instant).to_date_tuple(), sym454l)
      
      self.assertEqual(GregorianDate(Symmetry010(*sym010)).to_date_tuple(), gregorian)
      self.assertEqual(GregorianDate(Symmetry010LeapMonth(*sym010l)).to_date_tuple(), gregorian)
      self.assertEqual(GregorianDate(Symmetry454(*sym454)).to_date_tuple(), gregorian)
      self.assertEqual(GregorianDate(Symmetry454LeapMonth(*sym454l)).to_date_tuple(), gregorian)
    
    test((2025, 12, 28), (2025, 12, 28), (2025, 12, 28), (2025, 12, 28), (2025, 12, 28))
    test((2025, 12, 29), (2026, 1,  1 ), (2026, 1,  1 ), (2026, 1,  1 ), (2026, 1,  1 ))
    test((2026, 12, 27), (2026, 12, 30), (2026, 12, 30), (2026, 12, 28), (2026, 12, 28))
    test((2026, 12, 28), (2026, 12, 31), (2026, 13, 1 ), (2026, 12, 29), (2026, 13, 1 ))
    test((2026, 12, 29), (2026, 12, 32), (2026, 13, 2 ), (2026, 12, 30), (2026, 13, 2 ))
    test((2026, 12, 30), (2026, 12, 33), (2026, 13, 3 ), (2026, 12, 31), (2026, 13, 3 ))
    test((2026, 12, 31), (2026, 12, 34), (2026, 13, 4 ), (2026, 12, 32), (2026, 13, 4 ))
    test((2027, 1,  1 ), (2026, 12, 35), (2026, 13, 5 ), (2026, 12, 33), (2026, 13, 5 ))
    test((2027, 1,  2 ), (2026, 12, 36), (2026, 13, 6 ), (2026, 12, 34), (2026, 13, 6 ))
    test((2027, 1,  3 ), (2026, 12, 37), (2026, 13, 7 ), (2026, 12, 35), (2026, 13, 7 ))
    test((2027, 1,  4 ), (2027, 1,  1 ), (2027, 1,  1 ), (2027, 1,  1 ), (2027, 1,  1 ))
