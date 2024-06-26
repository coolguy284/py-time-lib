from enum import Enum
from numbers import Integral

from ..calendars.gregorian import GregorianDate

HOLIDAYS = Enum('HOLIDAYS', (
  'MOTHERS_DAY',
  'FATHERS_DAY',
))

def get_holiday(holiday: HOLIDAYS, year: Integral) -> GregorianDate:
  match holiday:
    case HOLIDAYS.MOTHERS_DAY:
      # https://en.wikipedia.org/wiki/Mother%27s_Day_(United_States)
      # second sunday in may
      return GregorianDate.from_month_week_day(year, 5, 2, 0)
    
    case HOLIDAYS.FATHERS_DAY:
      # https://en.wikipedia.org/wiki/Father%27s_Day_(United_States)
      # third sunday in june
      return GregorianDate.from_month_week_day(year, 6, 3, 0)

def get_holidays(year: Integral) -> list[tuple[str, GregorianDate]]:
  holidays = []
  
  for holiday in HOLIDAYS:
    holidays.append((holiday.name, get_holiday(holiday, year)))
  
  return holidays

def get_holidays_str(year: Integral) -> str:
  result = []
  
  for name, date in get_holidays(year):
    result.append(f'{name}: {date.to_iso_string()}')
  
  return '\n'.join(result)
