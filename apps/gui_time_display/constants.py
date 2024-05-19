from py_time_lib import LeapSmearPlan, LeapSmearSingle, LeapBasis, SmearType, FixedPrec, TimeInstant
from py_time_lib import APPROX_SECS_PER_YEAR

from enums import RunMode, TimeMode

# tweakables
time_mode = TimeMode.CUSTOMIZABLE
time_slider_absolute = False

run_mode = RunMode.TIME_STANDARDS

def get_run_mode() -> RunMode:
  global run_mode
  return run_mode

def set_run_mode(new_run_mode: RunMode) -> None:
  global run_mode
  run_mode = new_run_mode

# internal tweakables

# > window
width = 1280
height = 850

# > nav buttons
buttons_edge_x_coord = 40
buttons_y_coord = 40
buttons_size = 40

# > time sliders
time_sliders_edge_dist_x = 15
time_sliders_gap_y = 10
time_sliders_height = 60
time_sliders_reset_btn_width = 100

# >> time
time_min_exp = -5
time_max_exp = 17.8
time_linear_frac = 1 / (time_max_exp - time_min_exp + 1)

# >> time rate
time_rate_center_radius = 0.02
time_rate_min_exp = -5
time_rate_max_exp = 8
time_rate_linear_frac = 1 / (time_rate_max_exp - time_rate_min_exp + 1)
time_rate_text_size = 150

# > pages

# >> time standards
time_standards_format_str = '%a %b %d %Y %I:%M:%S.%.9f %p %:z'
time_standards_format_str_cap_offset = '%a %b %d %Y %I:%M:%S.%.9f %p %.10z'
time_standards_x_center_offset = 600
time_standards_y_start = 100
time_standards_y_step = 45

# >> calendar
calendars_time_format_str = '%I:%M:%S.%.9f %p'
calendars_format_str = f'%a %b %d %Y {calendars_time_format_str}'
calendars_x_center_offset = 600
calendars_y_start = 110
calendars_y_step = 60

# generated constants
smear_plan = LeapSmearPlan(
  LeapSmearSingle(
    start_basis = LeapBasis.START,
    secs_before_start_basis = 5,
    end_basis = LeapBasis.END,
    secs_after_end_basis = 5,
    type = SmearType.LINEAR
  ),
  ()
)
years_ago_epoch = TimeInstant.from_date_tuple_utc(1950, 1, 1, 0, 0, 0, 0).to_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME)
univ_start = TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME, years_ago_epoch - 13_800_000_000 * FixedPrec(APPROX_SECS_PER_YEAR))
earth_start = TimeInstant.from_secs_since_epoch_mono(TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME, years_ago_epoch - 4_540_000_000 * FixedPrec(APPROX_SECS_PER_YEAR))
