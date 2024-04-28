# py-time-lib

This is a time library for python that attempts to handle some of the complexities associated with time.

Features:
- Leap second support
- Support for dates arbitrarily far into the past or future (taking advantage of the unlimited size of python ints)

## Examples

Dates:

```python
>>> from py_time_lib import *

# Simple subtraction:
>>> GregorianDate(2024, 4, 26) - GregorianDate(2023, 12, 30)
DateDelta(118)

# Far dates:
>>> GregorianDate(2024, 4, 26) + DateDelta(10 ** 21)
GregorianDate(year = 2737907006988509659, month = 8, day = 28)
```

Times:

```python
>>> from py_time_lib import *

>>> t1 = TimeInstant.from_date_tuple_utc(
...   year=2024, month=4, day=26,
...   hour=13, minute=2, second=0,
...   frac_second=FixedPrec('0.01')
... )

# Internally stored as seconds since Jan 1, 1 BCE, Proleptic Gregorian Calendar:
>>> t1
TimeInstant(FixedPrec('63881355757.01'))

# Can handle dates in TAI or UTC format:
>>> t1.to_date_tuple_tai()
DateTupleBasic(
  year=2024, month=4, day=26,
  hour=13, minute=2, second=37,
  frac_second=FixedPrec('0.01')
)

>>> t1.to_date_tuple_utc()
DateTupleBasic(
  year=2024, month=4, day=26,
  hour=13, minute=2, second=0,
  frac_second=FixedPrec('0.01')
)

# T2 is right before the leap second at the end of 2016-12-31:
>>> t2 = TimeInstant.from_date_tuple_utc(
...   year=2016, month=12, day=31,
...   hour=23, minute=59, second=59,
...   frac_second=0
... )

>>> t2.to_date_tuple_utc()
DateTupleBasic(
  year=2016, month=12, day=31,
  hour=23, minute=59, second=59,
  frac_second=FixedPrec(0)
)

# One second later, UTC shows the 61st second of the minute:
>>> (t2 + TimeDelta(1)).to_date_tuple_utc()
DateTupleBasic(
  year=2016, month=12, day=31,
  hour=23, minute=59, second=60,
  frac_second=FixedPrec(0)
)

# Two seconds later, 2017 starts normally:
>>> (t2 + TimeDelta(2)).to_date_tuple_utc()
DateTupleBasic(
  year=2017, month=1, day=1,
  hour=0, minute=0, second=0,
  frac_second=FixedPrec(0)
)
```