from pathlib import Path
import os, sys

# https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
# https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
parent_dir = Path(os.path.realpath(__file__)).parent.parent
sys.path.append(str(parent_dir))

from enum import Enum
from functools import cache
import pygame
from py_time_lib import TimeInstant, FixedPrec, TIMEZONES, update_time_databases
from py_time_lib import LeapBasis, SmearType, LeapSmearSingle, LeapSmearPlan

update_time_databases()

if len(sys.argv) > 1:
  tz_name = sys.argv[1]
  if tz_name == 'None':
    tz_name = None
    tz = None
  elif tz_name == 'help':
    print('Timezones:')
    print(sorted(set([*TIMEZONES['proleptic_variable'], *TIMEZONES['proleptic_fixed']])))
    
    exit()
  else:
    try:
      tz = TIMEZONES['proleptic_variable'][tz_name]
    except KeyError:
      try:
        tz = TIMEZONES['proleptic_fixed'][tz_name]
      except KeyError:
        print(f'Timezone unknown: {tz_name}')
        exit()
  if len(sys.argv) > 2:
    longitude = FixedPrec(sys.argv[2])
  else:
    longitude = None
else:
  tz_name = None
  tz = None
  longitude = None

pygame.init()

width = 1280
height = 800
format_str_start = '%a %b %d %Y %I:%M:%S.%.9f %p'
format_str_offset = '%:z'
format_str = f'{format_str_start} {format_str_offset}'
smear_plan = LeapSmearPlan(
  LeapSmearSingle(
    start_basis = LeapBasis.START,
    secs_before_start_basis = 10,
    end_basis = LeapBasis.END,
    secs_after_end_basis = 0,
    type = SmearType.COSINE
  ),
  ()
)
RunMode = Enum('RunMode', (
  'CURRENT',
  'LEAP_SEC_REPLAY',
))
run_mode = RunMode.CURRENT

# https://stackoverflow.com/questions/11603222/allowing-resizing-window-pygame
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# https://stackoverflow.com/questions/40566585/how-to-change-the-name-of-a-pygame-window/40595418#40595418
pygame.display.set_caption('GUI Time Display')
refresh_rate = pygame.display.get_current_refresh_rate()
clock = pygame.time.Clock()

@cache
def get_font(font: str, size: int):
  return pygame.font.SysFont(font, size)

def draw_text_centered(
    surf: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    centered: bool = False,
    font: str = 'Consolas',
    size: int = 35,
    color: tuple[int, int, int] = (255, 255, 255)
  ) -> None:
  font = get_font(font, size)
  font_rendered = font.render(text, True, color)
  if centered:
    coords = (
      pos[0] - font_rendered.get_width() / 2,
      pos[1] - font_rendered.get_height() / 2
    )
  else:
    coords = pos
  surf.blit(font_rendered, coords)

def get_format_string_mono(now: TimeInstant, time_scale, pad_end = True):
  out_start = now.to_format_string_mono(time_scale, format_str_start)
  offset = now.to_format_string_mono(time_scale, format_str_offset)
  if '.' in offset:
    start, end = offset.split('.')
    if pad_end:
      offset = f'{start}.{end[:10]:0<10}'
    else:
      offset = f'{start}.{end[:10]}'
  elif pad_end:
    offset = f'{offset}.{'':0<10}'
  return f'{out_start} {offset}'

def get_format_string_solar(now: TimeInstant, longitude, true_solar, pad_end = True):
  out_start = now.to_format_string_solar(longitude, true_solar, format_str_start)
  offset = now.to_format_string_solar(longitude, true_solar, format_str_offset)
  if '.' in offset:
    start, end = offset.split('.')
    if pad_end:
      offset = f'{start}.{end[:10]:0<10}'
    else:
      offset = f'{start}.{end[:10]}'
  elif pad_end:
    offset = f'{offset}.{'':0<10}'
  return f'{out_start} {offset}'

loop = True

while loop:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      loop = False
  
  screen.fill((0, 0, 0))
  
  if run_mode == RunMode.CURRENT:
    now = TimeInstant.now()
  elif run_mode == RunMode.LEAP_SEC_REPLAY:
    now = TimeInstant(
      (
        TimeInstant.now().time -
        TimeInstant.from_date_tuple_utc(2024, 4, 28, 15, 28, 0, 0).time
      ) * 1 +
      TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 60, FixedPrec('0.994')).time
    )
  
  draw_text_centered(screen, 'Current Time', (width / 2, 50), centered = True, size = 43)
  
  x_center_offset = 600
  y_start = 130
  y_step = 55
  
  if tz != None:
    draw_text_centered(screen, f'TZ:  {now.to_format_string_tz(tz, format_str)}', (width / 2 - x_center_offset, y_start + 0 * y_step))
  draw_text_centered(screen, f'UTC: {now.to_format_string_utc(format_str)}', (width / 2 - x_center_offset, y_start + 1 * y_step))
  draw_text_centered(screen, f'TAI: {now.to_format_string_tai(format_str)}', (width / 2 - x_center_offset, y_start + 2 * y_step))
  draw_text_centered(screen, f'TT:  {get_format_string_mono(now, TimeInstant.TIME_SCALES.TT, pad_end = False)}', (width / 2 - x_center_offset, y_start + 3 * y_step))
  draw_text_centered(screen, f'TCG: {get_format_string_mono(now, TimeInstant.TIME_SCALES.TCG)}', (width / 2 - x_center_offset, y_start + 4 * y_step))
  draw_text_centered(screen, f'TCB: {get_format_string_mono(now, TimeInstant.TIME_SCALES.TCB)}', (width / 2 - x_center_offset, y_start + 5 * y_step))
  draw_text_centered(screen, f'GAL: {get_format_string_mono(now, TimeInstant.TIME_SCALES.GALACTIC_COORDINATE_TIME)}', (width / 2 - x_center_offset, y_start + 6 * y_step))
  draw_text_centered(screen, f'UNI: {get_format_string_mono(now, TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME)}', (width / 2 - x_center_offset, y_start + 7 * y_step))
  draw_text_centered(screen, f'UT1: {get_format_string_mono(now, TimeInstant.TIME_SCALES.UT1)}', (width / 2 - x_center_offset, y_start + 8 * y_step))
  if longitude != None:
    draw_text_centered(screen, f'MST: {get_format_string_solar(now, longitude, False)}', (width / 2 - x_center_offset, y_start + 9 * y_step))
    draw_text_centered(screen, f'TST: {get_format_string_solar(now, longitude, True)}', (width / 2 - x_center_offset, y_start + 10 * y_step))
  #draw_text_centered(screen, f'SUT: {now.to_format_string_smear_utc(smear_plan, format_str, true_utc_offset = True)}', (width / 2 - x_center_offset, y_start + 11 * y_step))
  if tz != None:
    pass#draw_text_centered(screen, f'STZ:  {now.to_format_string_smear_tz(smear_plan, tz, format_str, true_utc_offset = True)}', (width / 2 - x_center_offset, y_start + 12 * y_step))
  
  pygame.display.flip()
  clock.tick(refresh_rate)

pygame.quit()
