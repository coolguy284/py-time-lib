from ..fixed_prec import FixedPrec

NOMINAL_SECS_PER_DAY = 86_400

# data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
UTC_INITIAL_OFFSET_FROM_TAI: FixedPrec = FixedPrec(-10)
LEAP_SECONDS: list[tuple[str, FixedPrec, FixedPrec]] = [
  # (date, time in day, utc delta)
  ('1972-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1972-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1973-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1974-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1975-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1976-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1977-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1978-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1979-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1981-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1982-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1983-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1985-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1987-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1989-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1990-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1992-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1993-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1994-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1995-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1997-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('1998-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('2005-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('2008-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('2012-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('2015-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  ('2016-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
]
