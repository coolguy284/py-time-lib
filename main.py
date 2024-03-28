from py_time_lib.calendars.gregorian import GregorianDate
from py_time_lib.calendars.julian import JulianDate
from py_time_lib.fixed_prec import FixedPrec
from py_time_lib.time_classes import TimeInstant

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

t1 = TimeInstant(FixedPrec(1000, 0))
t2 = TimeInstant(FixedPrec(1003, 0))
print(t1)
print(t2)
print(t2 - t1)
print(t1 - t2)
print()

print(GregorianDate(2024, 3, 26).days_diff_from_julian())
print(GregorianDate(1900, 3, 1).days_diff_from_julian())
print(GregorianDate(1900, 2, 28).days_diff_from_julian())
print()

print(GregorianDate.from_iso_string('2024-03-27'))
print()
