from pathlib import Path
import os, sys

# https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
# https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
parent_dir = Path(os.path.realpath(__file__)).parent.parent
sys.path.append(str(parent_dir))

from functools import cache
import pygame
from py_time_lib import FixedPrec, TimeInstant, TimeDelta, TIMEZONES, update_time_databases

update_time_databases()

if len(sys.argv) > 1:
  tz_name = sys.argv[1]
  if tz_name == 'None':
    tz_name = None
    tz = None
  else:
    try:
      tz = TIMEZONES['proleptic_variable'][tz_name]
    except KeyError:
      try:
        tz = TIMEZONES['proleptic_fixed'][tz_name]
      except KeyError:
        print(f'Timezone unknown: {tz_name}')
        exit()
else:
  print('Timezones:')
  print(sorted(set([*TIMEZONES['proleptic_variable'], *TIMEZONES['proleptic_fixed']])))
  
  exit()

pygame.init()

width = 1280
height = 720
format_str = '%a %b %d %Y %I:%M:%S.%.9f %p %:z'

screen = pygame.display.set_mode((width, height))
refresh_rate = pygame.display.get_current_refresh_rate()
clock = pygame.time.Clock()

consolas = pygame.font.SysFont('Consolas', 35)

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

loop = True

while loop:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      loop = False
  
  screen.fill((0, 0, 0))
  
  # now = TimeInstant(
  #   (
  #     TimeInstant.now().time -
  #     TimeInstant.from_date_tuple_utc(2024, 4, 28, 15, 28, 0, 0).time
  #   ) * 1 +
  #   TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 60, FixedPrec('0.994')).time
  # )
  now = TimeInstant.now()
  
  draw_text_centered(screen, 'Current Time', (width / 2, 50), centered = True, size = 43)
  
  draw_text_centered(screen, f'TAI: {now.to_format_string_tai(format_str)}', (width / 2 - 480, 130))
  draw_text_centered(screen, f'UTC: {now.to_format_string_utc(format_str)}', (width / 2 - 480, 200))
  if tz != None:
    draw_text_centered(screen, f'TZ:  {now.to_format_string_tz(tz, format_str)}', (width / 2 - 480, 270))
  
  pygame.display.flip()
  clock.tick(refresh_rate)

pygame.quit()