from enum import Enum
from numbers import Integral

from ..calendars.gregorian import GregorianDate

HOLIDAYS = Enum('HOLIDAYS', (
  'NEW_YEARS_DAY',
  'MOTHERS_DAY',
  'MEMORIAL_DAY',
  'FATHERS_DAY',
  'US_INDEPENDENCE_DAY',
  'US_THANKSGIVING',
  'CHRISTMAS_EVE',
  'CHRISTMAS',
  'NEW_YEARS_EVE',
))

def get_holiday(holiday: HOLIDAYS, year: Integral) -> GregorianDate:
  match holiday:
    case HOLIDAYS.NEW_YEARS_DAY:
      # first day of the year
      return GregorianDate(year, 1, 1)
    
    case HOLIDAYS.MOTHERS_DAY:
      # https://en.wikipedia.org/wiki/Mother%27s_Day_(United_States)
      # second sunday in may
      return GregorianDate.from_month_week_day(year, 5, 2, 0)
    
    case HOLIDAYS.MEMORIAL_DAY:
      # https://en.wikipedia.org/wiki/Memorial_Day
      # last monday in may
      return GregorianDate.from_month_week_day(year, 5, 1, 1, True)
    
    case HOLIDAYS.FATHERS_DAY:
      # https://en.wikipedia.org/wiki/Father%27s_Day_(United_States)
      # third sunday in june
      return GregorianDate.from_month_week_day(year, 6, 3, 0)
    
    case HOLIDAYS.US_INDEPENDENCE_DAY:
      # july 4th
      return GregorianDate(year, 7, 4)
    
    case HOLIDAYS.US_THANKSGIVING:
      # https://en.wikipedia.org/wiki/Thanksgiving
      # 4th thursday in november
      return GregorianDate.from_month_week_day(year, 11, 4, 4)
    
    case HOLIDAYS.CHRISTMAS_EVE:
      # december 24th
      return GregorianDate(year, 12, 24)
    
    case HOLIDAYS.CHRISTMAS:
      # december 25th
      return GregorianDate(year, 12, 25)
    
    case HOLIDAYS.NEW_YEARS_EVE:
      # last day of the year
      return GregorianDate(year, 12, 31)

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
