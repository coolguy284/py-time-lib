def is_leap(year):
  return (year % 4 == 0) and not (year % 100 == 0) or (year % 400 == 0)

def num_days(year):
  return 366 if is_leap(year) else 365
