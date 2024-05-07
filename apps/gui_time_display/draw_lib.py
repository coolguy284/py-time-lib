from functools import cache
from pygame import Surface
from pygame.font import SysFont

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
    color: tuple[int, int, int] = (255, 255, 255)
  ) -> None:
  font = get_font(font, size)
  font_rendered = font.render(text, True, color)
  coords = (
    pos[0] - font_rendered.get_width() * horz_align,
    pos[1] - font_rendered.get_height() * vert_align,
  )
  surf.blit(font_rendered, coords)
