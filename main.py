from py_time_lib.calendars.gregorian import GregorianDate
from py_time_lib.calendars.julian import JulianDate

date_to_days_since_epoch = GregorianDate.date_to_days_since_epoch

print(date_to_days_since_epoch(1901, 1, 1) - date_to_days_since_epoch(1900, 1, 1))
print(date_to_days_since_epoch(2001, 1, 1) - date_to_days_since_epoch(2000, 1, 1))
print()

print(date_to_days_since_epoch(0, 1, 1))
print(date_to_days_since_epoch(0, 13, 1))
print(date_to_days_since_epoch(1, 1, 1))
print(date_to_days_since_epoch(0, 25, 1))
print(date_to_days_since_epoch(2, 1, 1))
print(date_to_days_since_epoch(0, 788 * 12 + 1, 1))
print(date_to_days_since_epoch(788, 1, 1))
print()

print(JulianDate.DAYS_IN_YEAR)
print(GregorianDate.DAYS_IN_YEAR)
print()
