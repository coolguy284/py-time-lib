import unittest

from ..calendars.iso_weekdate import IsoWeekDate

class TestCalendarIsoWeek(unittest.TestCase):
  def test_instantiate(self):
    IsoWeekDate(0)
