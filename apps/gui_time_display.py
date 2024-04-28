from pathlib import Path
import os, pygame, sys

# https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
# https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
parent_dir = Path(os.path.realpath(__file__)).parent.parent
sys.path.append(str(parent_dir))

from py_time_lib import TimeInstant

pygame.init()

width = 1280
height = 720
format_str = '%a %b %d %Y %I:%M:%S.%f %p'

screen = pygame.display.set_mode((width, height))
refresh_rate = pygame.display.get_current_refresh_rate()
clock = pygame.time.Clock()

consolas = pygame.font.SysFont('Consolas', 35)

def draw_centered(surf: pygame.Surface, font: pygame.font.Font, text: str, pos: tuple[int, int]) -> None:
  font_rendered = font.render(text, True, (255, 255, 255))
  coords = (
    pos[0] - font_rendered.get_width() / 2,
    pos[1] - font_rendered.get_height() / 2
  )
  surf.blit(font_rendered, coords)

loop = True

while loop:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      loop = False
  
  screen.fill((0, 0, 0))
  
  now = TimeInstant.now()
  
  draw_centered(screen, consolas, 'Current Time', (width / 2, 50))
  draw_centered(screen, consolas, f'TAI: {now.to_format_string_tai(format_str)}', (width / 2, 120))
  draw_centered(screen, consolas, f'UTC: {now.to_format_string_utc(format_str)}', (width / 2, 190))
  
  pygame.display.flip()
  clock.tick(refresh_rate)

pygame.quit()
