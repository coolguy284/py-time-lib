from .gregorian import GregorianDate

class HoloceneDate(GregorianDate):
  '''
  Class for holocene dates. The holocene calendar years are precisely
  10,000 greater than gregorian years. For example, gregorian year 2024
  is holocene year 12024.
  '''
  __slots__ = ()
  JAN_1_YEAR0_DAY_OFFSET = GregorianDate.JAN_1_YEAR0_DAY_OFFSET - (10000 // GregorianDate.REPEAT_PERIOD_YEARS * GregorianDate.REPEAT_PERIOD_DAYS)
