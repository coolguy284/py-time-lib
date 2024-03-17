def is_leap(year):
  return year % 4 == 0

def num_days(year):
  return 366 if is_leap(year) else 365
