from ..constants import NOMINAL_SECS_PER_HOUR
from ..calendars.gregorian import GregorianDate
from ..time_classes.time_instant.time_inst_smear import LeapBasis, SmearType, LeapSmearSingle, LeapSmearPlan

PAUSE = LeapSmearPlan(
  LeapSmearSingle(
    start_basis = LeapBasis.START,
    secs_before_start_basis = 0,
    end_basis = LeapBasis.END,
    secs_after_end_basis = 0,
    type = SmearType.LINEAR
  ),
  {}
)

# https://developers.google.com/time/smear
NOON_TO_NOON = LeapSmearPlan(
  LeapSmearSingle(
    start_basis = LeapBasis.START,
    secs_before_start_basis = 12 * NOMINAL_SECS_PER_HOUR,
    end_basis = LeapBasis.END,
    secs_after_end_basis = 12 * NOMINAL_SECS_PER_HOUR,
    type = SmearType.LINEAR
  ),
  {}
)

# https://developers.google.com/time/smear
TWENTY_HOUR_CENTERED = LeapSmearPlan(
  LeapSmearSingle(
    start_basis = LeapBasis.START,
    secs_before_start_basis = 10 * NOMINAL_SECS_PER_HOUR,
    end_basis = LeapBasis.END,
    secs_after_end_basis = 10 * NOMINAL_SECS_PER_HOUR,
    type = SmearType.LINEAR
  ),
  {}
)

# https://developers.google.com/time/smear
UTC_SLS = LeapSmearPlan(
  LeapSmearSingle(
    start_basis = LeapBasis.START,
    secs_before_start_basis = 1_000,
    end_basis = LeapBasis.END,
    secs_after_end_basis = 0,
    type = SmearType.LINEAR
  ),
  {}
)

# https://developers.google.com/time/smear
GOOGLE = LeapSmearPlan(
  NOON_TO_NOON.default_smear,
  {
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1972-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1972-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1973-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1974-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1975-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1976-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1977-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1978-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1979-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1981-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1982-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1983-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1985-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1987-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1989-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1990-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1992-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1993-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1994-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1995-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1997-06-30')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('1998-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('2005-12-31')): PAUSE.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('2008-12-31')): LeapSmearSingle(
      start_basis = LeapBasis.START,
      secs_before_start_basis = 20 * NOMINAL_SECS_PER_HOUR,
      end_basis = LeapBasis.END,
      secs_after_end_basis = 0,
      type = SmearType.COSINE
    ),
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('2012-06-30')): TWENTY_HOUR_CENTERED.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('2015-06-30')): TWENTY_HOUR_CENTERED.default_smear,
    LeapSmearPlan.date_to_tai_start(GregorianDate.from_iso_string('2016-12-31')): TWENTY_HOUR_CENTERED.default_smear,
  }
)
