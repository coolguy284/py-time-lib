from abc import abstractmethod, ABC
from enum import Enum
from pygame import Surface
from pygame.draw import line as draw_line, rect as draw_rect

from draw_lib import draw_text_centered

class PositionalElement(ABC):
  __slots__ = 'screen', 'x', 'y', 'w', 'h'
  screen: Surface
  x: float
  y: float
  w: float
  h: float
  
  def __init__(self, screen: Surface, x: float, y: float, w: float, h: float):
    self.screen = screen
    self.x = x
    self.y = y
    self.w = w
    self.h = h
  
  @abstractmethod
  def draw(self) -> None:
    ...

class Button(PositionalElement):
  __slots__ = 'text', 'size', 'enabled'
  text: str
  size: int
  enabled: bool
  
  button_disabled_color = 127, 127, 127
  button_active_color = 255, 255, 255
    
  def __init__(self, screen: Surface, x: float, y: float, w: float, h: float, text: str, size: int):
    super().__init__(screen, x, y, w, h)
    self.text = text
    self.size = size
    self.enabled = False
  
  def draw(self) -> None:
    draw_rect(
      self.screen,
      Button.button_active_color if self.enabled else Button.button_disabled_color,
      (self.x, self.y, self.w, self.h),
      width = 2,
      border_top_left_radius = 4,
      border_top_right_radius = 4,
      border_bottom_left_radius = 4,
      border_bottom_right_radius = 4
    )
    draw_text_centered(
      self.screen,
      self.text,
      (self.x + self.w / 2, self.y + self.h / 2),
      horz_align = 0.5,
      vert_align = 0.4,
      size = self.size
    )
  
  def is_pressed(self, mouse_click_pos: tuple[float, float]) -> bool:
    if self.enabled:
      if self.x < mouse_click_pos[0] < self.x + self.w and self.y < mouse_click_pos[1] < self.y + self.h:
        return True
      else:
        return False
    else:
      return False

class Slider(PositionalElement):
  __slots__ = 'orientation', 'value'
  
  Orientation = Enum('SliderOrientation', (
    'HORIZONTAL',
    'VERTICAL'
  ))
  
  orientation: Orientation
  value: float
  
  line_margin = 1
  
  def __init__(self, screen: Surface, x: float, y: float, w: float, h: float, orientation: Orientation):
    super().__init__(screen, x, y, w, h)
    self.orientation = orientation
    self.value = 0
  
  def draw(self) -> None:
    draw_rect(
      self.screen,
      (255, 255, 255),
      (self.x, self.y, self.w, self.h),
      width = 2,
      border_top_left_radius = 4,
      border_top_right_radius = 4,
      border_bottom_left_radius = 4,
      border_bottom_right_radius = 4
    )
    if self.orientation == self.Orientation.HORIZONTAL:
      draw_line(
        self.screen,
        (255, 255, 255),
        (self.x + self.w * self.value, self.y + self.line_margin),
        (self.x + self.w * self.value, self.y + self.h - self.line_margin),
        width = 2
      )
    else:
      draw_line(
        self.screen,
        (255, 255, 255),
        (self.x + self.line_margin, self.y + self.h * self.value),
        (self.x + self.w - self.line_margin, self.y + self.h * self.value),
        width = 2
      )
  
  def is_pressed(self, mouse_click_pos: tuple[float, float]) -> tuple[bool, float | None]:
    if self.x < mouse_click_pos[0] < self.x + self.w and self.y < mouse_click_pos[1] < self.y + self.h:
      if self.orientation == self.Orientation.HORIZONTAL:
        return True, (mouse_click_pos[0] - self.x) / self.w
      else:
        return True, (mouse_click_pos[1] - self.y) / self.h
    else:
      return False, None
