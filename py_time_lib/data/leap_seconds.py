from ..fixed_prec import FixedPrec

# data from https://www.nist.gov/pml/time-and-frequency-division/time-realization/leap-seconds
LEAP_SECONDS: list[tuple[str, FixedPrec]] = [
  # (date, utc delta)
  ('1972-06-30', FixedPrec(-1, 0)),
  ('1972-12-31', FixedPrec(-1, 0)),
  ('1973-12-31', FixedPrec(-1, 0)),
  ('1974-12-31', FixedPrec(-1, 0)),
  ('1975-12-31', FixedPrec(-1, 0)),
  ('1976-12-31', FixedPrec(-1, 0)),
  ('1977-12-31', FixedPrec(-1, 0)),
  ('1978-12-31', FixedPrec(-1, 0)),
  ('1979-12-31', FixedPrec(-1, 0)),
  ('1981-06-30', FixedPrec(-1, 0)),
  ('1982-06-30', FixedPrec(-1, 0)),
  ('1983-06-30', FixedPrec(-1, 0)),
  ('1985-06-30', FixedPrec(-1, 0)),
  ('1987-12-31', FixedPrec(-1, 0)),
  ('1989-12-31', FixedPrec(-1, 0)),
  ('1990-12-31', FixedPrec(-1, 0)),
  ('1992-06-30', FixedPrec(-1, 0)),
  ('1993-06-30', FixedPrec(-1, 0)),
  ('1994-06-30', FixedPrec(-1, 0)),
  ('1995-12-31', FixedPrec(-1, 0)),
  ('1997-06-30', FixedPrec(-1, 0)),
  ('1998-12-31', FixedPrec(-1, 0)),
  ('2005-12-31', FixedPrec(-1, 0)),
  ('2008-12-31', FixedPrec(-1, 0)),
  ('2012-06-30', FixedPrec(-1, 0)),
  ('2015-06-30', FixedPrec(-1, 0)),
  ('2016-12-31', FixedPrec(-1, 0)),
]
