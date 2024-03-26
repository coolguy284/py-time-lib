from py_time_lib.calendars.gregorian import date_to_days_since_epoch

print(date_to_days_since_epoch(1901, 1, 1) - date_to_days_since_epoch(1900, 1, 1))
print(date_to_days_since_epoch(2001, 1, 1) - date_to_days_since_epoch(2000, 1, 1))
