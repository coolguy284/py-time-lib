from ..constants import NOMINAL_SECS_PER_DAY
from ..named_tuples import LeapSecEntry
from ..fixed_prec import FixedPrec

# data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
UTC_INITIAL_OFFSET_FROM_TAI: FixedPrec = FixedPrec(-10)
LEAP_SECONDS: list[LeapSecEntry] = [
  # (date, time in day, utc delta)
  LeapSecEntry('1972-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1972-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1973-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1974-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1975-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1976-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1977-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1978-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1979-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1981-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1982-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1983-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1985-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1987-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1989-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1990-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1992-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1993-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1994-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1995-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1997-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('1998-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('2005-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('2008-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('2012-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('2015-06-30', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
  LeapSecEntry('2016-12-31', FixedPrec(NOMINAL_SECS_PER_DAY), FixedPrec(-1)),
]
