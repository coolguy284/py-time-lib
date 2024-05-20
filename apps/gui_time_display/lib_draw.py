from functools import cache
from math import hypot
from pygame import Surface
from pygame.font import SysFont
from pygame.transform import rotate
from pygame.gfxdraw import aapolygon, filled_polygon, aacircle, filled_circle

@cache
def get_font(font: str, size: int):
  return SysFont(font, size)

def draw_text_centered(
    surf: Surface,
    text: str,
    pos: tuple[int, int],
    horz_align: float = 0.0,
    vert_align: float = 0.5,
    font: str = 'Consolas',
    size: int = 35,
    color: tuple[int, int, int] = (255, 255, 255),
    rotation: float = 0
  ) -> None:
  font = get_font(font, size)
  font_rendered = font.render(text, True, color)
  if rotation != 0:
    font_rendered = rotate(font_rendered, rotation)
  coords = (
    pos[0] - font_rendered.get_width() * horz_align,
    pos[1] - font_rendered.get_height() * vert_align,
  )
  surf.blit(font_rendered, coords)

def thick_aaline(surf: Surface, start_pos, end_pos, color, width):
  start_to_end = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
  transverse_dir = [-start_to_end[1], start_to_end[0]]
  factor = hypot(*transverse_dir)
  transverse_dir[0] /= factor
  transverse_dir[1] /= factor
  points = (
    (start_pos[0] + transverse_dir[0] * width, start_pos[1] + transverse_dir[1] * width),
    (start_pos[0] - transverse_dir[0] * width, start_pos[1] - transverse_dir[1] * width),
    (end_pos[0] - transverse_dir[0] * width, end_pos[1] - transverse_dir[1] * width),
    (end_pos[0] + transverse_dir[0] * width, end_pos[1] + transverse_dir[1] * width)
  )
  filled_polygon(surf, points, color)
  aapolygon(surf, points, color)
  start_pos_int = int(start_pos[0]), int(start_pos[1])
  end_pos_int = int(end_pos[0]), int(end_pos[1])
  filled_circle(surf, *start_pos_int, width, color)
  aacircle(surf, *start_pos_int, width, color)
  filled_circle(surf, *end_pos_int, width, color)
  aacircle(surf, *end_pos_int, width, color)

class PolarDrawer:
  def __init__(self):
    ...
