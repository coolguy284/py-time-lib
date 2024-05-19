# https://stackoverflow.com/questions/28379664/iife-in-python-common-convention/76936985#76936985
@lambda func: func()
def fix_import_path():
  from pathlib import Path
  from os.path import realpath
  from sys import path as sys_path

  # https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
  # https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
  parent_dir = Path(realpath(__file__)).parent.parent.parent
  sys_path.append(str(parent_dir))

from asyncio import TaskGroup, run
from enum import Enum
from math import ceil, floor, log10
from sys import argv as sys_argv
import pygame
from py_time_lib import FixedPrec, TimeInstant, TimeDelta, JulianDate, GregorianDate, IsoWeekDate, HoloceneDate, Symmetry010, Symmetry010LeapMonth, Symmetry454, Symmetry454LeapMonth
from py_time_lib import TIMEZONES, update_time_databases, update_time_databases_loop
from py_time_lib import LeapBasis, SmearType, LeapSmearSingle, LeapSmearPlan
from py_time_lib.constants import NOMINAL_SECS_PER_MIN, NOMINAL_SECS_PER_HOUR, NOMINAL_SECS_PER_DAY, NOMINAL_SECS_PER_WEEK, APPROX_SECS_PER_MONTH, APPROX_SECS_PER_YEAR, NOMINAL_MILLISECS_PER_SEC, NOMINAL_MICROSECS_PER_SEC

from draw_lib import draw_text_centered
from advanced_clock import AdvancedClock
from ui_components import Button, Slider

async def main():
  update_time_databases()
  
  if len(sys_argv) > 1:
    tz_name = sys_argv[1]
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
    if len(sys_argv) > 2:
      longitude = FixedPrec(sys_argv[2])
    else:
      longitude = None
  else:
    tz_name = None
    tz = None
    longitude = None
  
  pygame.init()
  
  width = 1280
  height = 850
  buttons_edge_x_coord = 40
  buttons_y_coord = 40
  buttons_size = 40
  time_sliders_edge_dist_x = 15
  time_sliders_gap_y = 10
  time_rate_text_size = 150
  time_sliders_height = 60
  time_sliders_reset_btn_width = 100
  time_standards_format_str = '%a %b %d %Y %I:%M:%S.%.9f %p %:z'
  time_standards_format_str_cap_offset = '%a %b %d %Y %I:%M:%S.%.9f %p %.10z'
  time_standards_x_center_offset = 600
  time_standards_y_start = 100
  time_standards_y_step = 45
  time_min_exp = -5
  time_max_exp = 17.8
  time_linear_frac = 1 / (time_max_exp - time_min_exp + 1)
  time_rate_center_radius = 0.02
  time_rate_min_exp = -5
  time_rate_max_exp = 8
  time_rate_linear_frac = 1 / (time_rate_max_exp - time_rate_min_exp + 1)
  calendars_time_format_str = '%I:%M:%S.%.9f %p'
  calendars_format_str = f'%a %b %d %Y {calendars_time_format_str}'
  calendars_x_center_offset = 600
  calendars_y_start = 110
  calendars_y_step = 60
  
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
  TimeMode = Enum('TimeMode', (
    'CURRENT',
    'LEAP_SEC_REPLAY',
    'CUSTOMIZABLE',
  ))
  time_mode = TimeMode.CUSTOMIZABLE
  time_slider_absolute = True
  RunMode = Enum('RunMode', (
    'CLOCK',
    'TIME_STANDARDS',
    'CALENDARS',
    'BLANK',
  ))
  run_modes = list(RunMode)
  run_mode_names = {
    RunMode.CLOCK: 'Clock',
    RunMode.TIME_STANDARDS: 'Time Standards',
    RunMode.CALENDARS: 'Calendars (UTC)',
    RunMode.BLANK: 'Blank',
  }
  run_mode = RunMode.TIME_STANDARDS
  dragging_time_slider = False
  dragging_time_rate_slider = False
  
  # https://stackoverflow.com/questions/11603222/allowing-resizing-window-pygame
  screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
  # https://stackoverflow.com/questions/40566585/how-to-change-the-name-of-a-pygame-window/40595418#40595418
  pygame.display.set_caption('GUI Time Display')
  refresh_rate = pygame.display.get_current_refresh_rate()
  clock = AdvancedClock()
  
  def linear_to_exponential(linear_start_frac: float, min_exp: float, max_exp: float, value: float) -> FixedPrec:
    if value <= linear_start_frac:
      return FixedPrec(10) ** min_exp * value / linear_start_frac
    else:
      return FixedPrec(10) ** (
        min_exp +
        (value - linear_start_frac) /
        (1 - linear_start_frac) *
        (max_exp - min_exp)
      )
  
  def exponential_to_linear(linear_start_frac: float, min_exp: float, max_exp: float, value: FixedPrec) -> float:
    lin_threshold = FixedPrec(10) ** min_exp
    if value <= lin_threshold:
      return float(value / lin_threshold) * linear_start_frac
    else:
      return linear_start_frac + \
        (log10(value) - min_exp) / (max_exp - min_exp) * (1 - linear_start_frac)
  
  def time_rate_true_to_norm(time_rate: FixedPrec) -> float:
    if time_rate == 0:
      return 0.5
    else:
      forwards = time_rate > 0
      mul = 1 if forwards else -1
      rate_abs = abs(time_rate)
      norm_abs = exponential_to_linear(time_rate_linear_frac, time_rate_min_exp, time_rate_max_exp, rate_abs)
      return 0.5 + mul * (norm_abs * (0.5 - time_rate_center_radius) + time_rate_center_radius)
  
  def time_rate_norm_to_true(time_rate_norm: float) -> tuple[FixedPrec, float]:
    if 0.5 - time_rate_center_radius / 2 < time_rate_norm < 0.5 + time_rate_center_radius / 2:
      return FixedPrec(0), 0.5
    else:
      forwards = time_rate_norm > 0.5
      mul = 1 if forwards else -1
      norm_abs = max(
        (abs(time_rate_norm - 0.5) - time_rate_center_radius) / (0.5 - time_rate_center_radius),
        0
      )
      return (
        mul * linear_to_exponential(time_rate_linear_frac, time_rate_min_exp, time_rate_max_exp, norm_abs),
        0.5 + mul * (norm_abs * (0.5 - time_rate_center_radius) + time_rate_center_radius),
      )
  
  def time_norm_to_true_delta(time_norm: float) -> FixedPrec:
    norm_abs = abs(time_norm - 0.5) * 2
    positive = time_norm >= 0.5
    mul = 1 if positive else -1
    return mul * linear_to_exponential(time_linear_frac, time_min_exp, time_max_exp, norm_abs)
  
  def time_delta_to_time_norm(time_delta: FixedPrec) -> float:
    delta_abs = abs(time_delta)
    mul = 1 if time_delta >= 0 else -1
    norm_abs = exponential_to_linear(time_linear_frac, time_min_exp, time_max_exp, delta_abs)
    return (mul * norm_abs) * 0.5 + 0.5
  
  loop = True
  
  if time_mode == TimeMode.LEAP_SEC_REPLAY:
    prgm_start_secs = TimeInstant.now().time
  elif time_mode == TimeMode.CUSTOMIZABLE:
    time_reset_time = TimeInstant.now().time
    time_base = time_reset_time
    time_rate = FixedPrec(1)
    old_time_rate = None
    old_time_base = None
    time_delta = None
    
    def reset_time_base_to_current() -> None:
      nonlocal time_base, time_reset_time
      time_base = now.time
      time_reset_time = true_now.time
  
  left_btn = Button(
    screen = screen,
    x = None,
    y = None,
    w = None,
    h = None,
    text = '<',
    size = 40
  )
  right_btn = Button(
    screen = screen,
    x = None,
    y = None,
    w = None,
    h = None,
    text = '>',
    size = 40
  )
  
  if time_mode == TimeMode.CUSTOMIZABLE:
    time_slider = Slider(
      screen = screen,
      x = None,
      y = None,
      w = None,
      h = None,
      orientation = Slider.Orientation.HORIZONTAL
    )
    time_slider.value = 0.5
    
    time_reset_btn = Button(
      screen = screen,
      x = None,
      y = None,
      w = None,
      h = None,
      text = 'Reset',
      size = 35
    )
    time_reset_btn.enabled = True
    
    time_rate_slider = Slider(
      screen = screen,
      x = None,
      y = None,
      w = None,
      h = None,
      orientation = Slider.Orientation.HORIZONTAL
    )
    time_rate_slider.value = time_rate_true_to_norm(time_rate)
    
    time_rate_reset_btn = Button(
      screen = screen,
      x = None,
      y = None,
      w = None,
      h = None,
      text = 'Reset',
      size = 35
    )
    time_rate_reset_btn.enabled = True
    
    def draw_time_rate_line_raw(surf: pygame.Surface, norm_x, color = (127, 127, 127), width = 1) -> None:
      pygame.draw.line(
        surf,
        color,
        time_rate_slider.local_to_subworld(norm_x, 0, True),
        time_rate_slider.local_to_subworld(norm_x, 1, True),
        width = width
      )
    
    def draw_time_rate_line(surf: pygame.Surface, value, color = (127, 127, 127), width = 1) -> None:
      draw_time_rate_line_raw(
        surf,
        time_rate_true_to_norm(value),
        color,
        width
      )
    
    def draw_time_rate_text(surf: pygame.Surface, value) -> None:
      draw_text_centered(
        surf,
        f'{value:g}x',
        time_rate_slider.local_to_subworld(
          time_rate_true_to_norm(value),
          0.5
        ),
        horz_align = 0.8 if value < 0 else 0,
        size = 10,
        rotation = 90 if value < 0 else -90
      )
    
    def draw_time_delta_line(surf: pygame.Surface, value, color = (127, 127, 127), width = 1) -> None:
      norm_x = time_delta_to_time_norm(value)
      pygame.draw.line(
        surf,
        color,
        time_slider.local_to_subworld(norm_x, 0, True),
        time_slider.local_to_subworld(norm_x, 1, True),
        width = width
      )
    
    def draw_time_delta_line_true(surf: pygame.Surface, value, color = (127, 127, 127), width = 1) -> None:
      norm_x = time_delta_to_time_norm(value)
      pygame.draw.line(
        surf,
        color,
        time_slider.local_to_world(norm_x, 0, True),
        time_slider.local_to_world(norm_x, 0.95, True),
        width = width
      )
    
    def draw_time_delta_text(surf: pygame.Surface, value, value_str: str) -> None:
      draw_text_centered(
        surf,
        value_str,
        time_slider.local_to_subworld(
          time_delta_to_time_norm(value),
          0.5
        ),
        horz_align = 0.8 if value < 0 else 0,
        size = 10,
        rotation = 90 if value < 0 else -90
      )
    
    def draw_time_delta_text_true(surf: pygame.Surface, value, value_str: str) -> None:
      draw_text_centered(
        surf,
        value_str,
        time_slider.local_to_world(
          time_delta_to_time_norm(value),
          0.5
        ),
        horz_align = 0.8 if value < 0 else 0,
        size = 10,
        rotation = 90 if value < 0 else -90
      )
    
    def get_time_rate_slider_surface() -> pygame.Surface:
      result = pygame.Surface((time_rate_slider.w, time_rate_slider.h))
      
      draw_time_rate_line(result, 0, (255, 255, 255))
      draw_time_rate_line_raw(result, 0.5 + time_rate_center_radius, (255, 255, 255))
      draw_time_rate_line_raw(result, 0.5 - time_rate_center_radius, (255, 255, 255))
      for i in range(1, 10):
        num = 10 ** time_rate_min_exp * (i / 10)
        draw_time_rate_line(result, num)
        draw_time_rate_line(result, -num)
      for exp in range(time_rate_min_exp, ceil(time_rate_max_exp), 1):
        draw_time_rate_line(result, 10 ** exp, (255, 255, 255))
        draw_time_rate_line(result, -10 ** exp, (255, 255, 255))
        draw_time_rate_text(result, 10 ** exp)
        draw_time_rate_text(result, -10 ** exp)
        for i in range(2, 10):
          num = 10 ** exp * i
          if log10(num) > time_rate_max_exp:
            break
          draw_time_rate_line(result, num)
          draw_time_rate_line(result, -num)
      
      return result
    
    def get_time_slider_delta_surface() -> pygame.Surface:
      result = pygame.Surface((time_slider.w, time_slider.h))
      
      draw_time_delta_line(result, 0, (255, 255, 255))
      
      for exp in range(3):
        us = 10 ** exp
        num_base = us / NOMINAL_MICROSECS_PER_SEC
        
        if exp != 0:
          draw_time_delta_line(result, num_base, (255, 255, 255))
          draw_time_delta_line(result, -num_base, (255, 255, 255))
          draw_time_delta_text(result, num_base, f'{us:g}us')
          draw_time_delta_text(result, -num_base, f'-{us:g}us')
        
        for i in range(2 if exp != 0 else 1, 10):
          draw_time_delta_line(result, num_base * i)
          draw_time_delta_line(result, -num_base * i)
      
      for exp in range(3):
        ms = 10 ** exp
        num_base = ms / NOMINAL_MILLISECS_PER_SEC
        draw_time_delta_line(result, num_base, (255, 255, 255))
        draw_time_delta_line(result, -num_base, (255, 255, 255))
        draw_time_delta_text(result, num_base, f'{ms:g}ms')
        draw_time_delta_text(result, -num_base, f'-{ms:g}ms')
        
        for i in range(2, 10):
          draw_time_delta_line(result, num_base * i)
          draw_time_delta_line(result, -num_base * i)
      
      draw_time_delta_line(result, 1, (255, 255, 255))
      draw_time_delta_line(result, -1, (255, 255, 255))
      draw_time_delta_text(result, 1, '1s')
      draw_time_delta_text(result, -1, '-1s')
      for i in range(2, 10):
        draw_time_delta_line(result, i)
        draw_time_delta_line(result, -i)
      
      draw_time_delta_line(result, 10, (255, 255, 255))
      draw_time_delta_line(result, -10, (255, 255, 255))
      draw_time_delta_text(result, 10, '10s')
      draw_time_delta_text(result, -10, '-10s')
      draw_time_delta_line(result, 15)
      draw_time_delta_line(result, -15)
      for i in range(2, 4):
        draw_time_delta_line(result, 15 * i)
        draw_time_delta_line(result, -15 * i)
      
      draw_time_delta_line(result, NOMINAL_SECS_PER_MIN, (255, 255, 255))
      draw_time_delta_line(result, -NOMINAL_SECS_PER_MIN, (255, 255, 255))
      draw_time_delta_text(result, NOMINAL_SECS_PER_MIN, '1m')
      draw_time_delta_text(result, -NOMINAL_SECS_PER_MIN, '-1m')
      for i in range(2, 10):
        draw_time_delta_line(result, NOMINAL_SECS_PER_MIN * i)
        draw_time_delta_line(result, -NOMINAL_SECS_PER_MIN * i)
      
      draw_time_delta_line(result, 10 * NOMINAL_SECS_PER_MIN, (255, 255, 255))
      draw_time_delta_line(result, -10 * NOMINAL_SECS_PER_MIN, (255, 255, 255))
      draw_time_delta_text(result, 10 * NOMINAL_SECS_PER_MIN, '10m')
      draw_time_delta_text(result, -10 * NOMINAL_SECS_PER_MIN, '-10m')
      draw_time_delta_line(result, 15 * NOMINAL_SECS_PER_MIN)
      draw_time_delta_line(result, -15 * NOMINAL_SECS_PER_MIN)
      for i in range(2, 4):
        draw_time_delta_line(result, 15 * NOMINAL_SECS_PER_MIN * i)
        draw_time_delta_line(result, -15 * NOMINAL_SECS_PER_MIN * i)
      
      draw_time_delta_line(result, NOMINAL_SECS_PER_HOUR, (255, 255, 255))
      draw_time_delta_line(result, -NOMINAL_SECS_PER_HOUR, (255, 255, 255))
      draw_time_delta_text(result, NOMINAL_SECS_PER_HOUR, '1h')
      draw_time_delta_text(result, -NOMINAL_SECS_PER_HOUR, '-1h')
      for i in range(2, 10):
        draw_time_delta_line(result, NOMINAL_SECS_PER_HOUR * i)
        draw_time_delta_line(result, -NOMINAL_SECS_PER_HOUR * i)
      
      draw_time_delta_line(result, 10 * NOMINAL_SECS_PER_HOUR, (255, 255, 255))
      draw_time_delta_line(result, -10 * NOMINAL_SECS_PER_HOUR, (255, 255, 255))
      draw_time_delta_text(result, 10 * NOMINAL_SECS_PER_HOUR, '10h')
      draw_time_delta_text(result, -10 * NOMINAL_SECS_PER_HOUR, '-10h')
      draw_time_delta_line(result, 12 * NOMINAL_SECS_PER_HOUR)
      draw_time_delta_line(result, -12 * NOMINAL_SECS_PER_HOUR)
      
      draw_time_delta_line(result, NOMINAL_SECS_PER_DAY, (255, 255, 255))
      draw_time_delta_line(result, -NOMINAL_SECS_PER_DAY, (255, 255, 255))
      draw_time_delta_text(result, NOMINAL_SECS_PER_DAY, '1d')
      draw_time_delta_text(result, -NOMINAL_SECS_PER_DAY, '-1d')
      
      for i in range(2, 7):
        draw_time_delta_line(result, NOMINAL_SECS_PER_DAY * i)
        draw_time_delta_line(result, -NOMINAL_SECS_PER_DAY * i)
      
      draw_time_delta_line(result, NOMINAL_SECS_PER_WEEK, (255, 255, 255))
      draw_time_delta_line(result, -NOMINAL_SECS_PER_WEEK, (255, 255, 255))
      draw_time_delta_text(result, NOMINAL_SECS_PER_WEEK, '1wk')
      draw_time_delta_text(result, -NOMINAL_SECS_PER_WEEK, '-1wk')
      
      for i in range(2, 4):
        draw_time_delta_line(result, NOMINAL_SECS_PER_WEEK * i)
        draw_time_delta_line(result, -NOMINAL_SECS_PER_WEEK * i)
      
      draw_time_delta_line(result, APPROX_SECS_PER_MONTH, (255, 255, 255))
      draw_time_delta_line(result, -APPROX_SECS_PER_MONTH, (255, 255, 255))
      draw_time_delta_text(result, APPROX_SECS_PER_MONTH, '1mo')
      draw_time_delta_text(result, -APPROX_SECS_PER_MONTH, '-1mo')
      
      for i in range(2, 12):
        draw_time_delta_line(result, APPROX_SECS_PER_MONTH * i)
        draw_time_delta_line(result, -APPROX_SECS_PER_MONTH * i)
      
      exp = 0
      
      while True:
        years = 10 ** exp
        num_base = APPROX_SECS_PER_YEAR * years
        draw_time_delta_line(result, num_base, (255, 255, 255))
        draw_time_delta_line(result, -num_base, (255, 255, 255))
        draw_time_delta_text(result, num_base, f'{years:g}y')
        draw_time_delta_text(result, -num_base, f'-{years:g}y')
        
        for i in range(2, 10):
          draw_time_delta_line(result, num_base * i)
          draw_time_delta_line(result, -num_base * i)
          
          if log10(num_base * i) > time_max_exp:
            break
        else:
          exp += 1
          continue
        
        break
      
      return result
    
    time_details = None
    time_rate_details = None
    
    def draw_time_line_true(instant: TimeInstant, string: str) -> None:
      time_delta = (instant - visual_time).time_delta
      draw_time_delta_line_true(screen, time_delta, (255, 255, 255))
      draw_time_delta_text_true(screen, time_delta, string)
  
  def recalculate_vars_after_resize():
    left_btn.x = buttons_edge_x_coord - buttons_size / 2
    left_btn.y = buttons_y_coord - buttons_size / 2
    left_btn.w = buttons_size
    left_btn.h = buttons_size
    
    right_btn.x = width - buttons_edge_x_coord - buttons_size / 2
    right_btn.y = buttons_y_coord - buttons_size / 2
    right_btn.w = buttons_size
    right_btn.h = buttons_size
    
    if time_mode == TimeMode.CUSTOMIZABLE:
      nonlocal time_details, time_rate_details
      
      time_slider.x = time_sliders_edge_dist_x
      time_slider.y = height - time_sliders_height * 2 - time_sliders_gap_y * 2
      time_slider.w = width - time_sliders_reset_btn_width - time_sliders_edge_dist_x * 2
      time_slider.h = time_sliders_height
      
      time_reset_btn.x = width - time_sliders_reset_btn_width - time_sliders_edge_dist_x
      time_reset_btn.y = height - time_sliders_height * 2 - time_sliders_gap_y * 2
      time_reset_btn.w = time_sliders_reset_btn_width
      time_reset_btn.h = time_sliders_height
      
      time_rate_slider.x = time_sliders_edge_dist_x
      time_rate_slider.y = height - time_sliders_height - time_sliders_gap_y
      time_rate_slider.w = width - time_sliders_reset_btn_width - time_rate_text_size - time_sliders_edge_dist_x * 2
      time_rate_slider.h = time_sliders_height
      
      time_rate_reset_btn.x = width - time_sliders_reset_btn_width - time_rate_text_size - time_sliders_edge_dist_x
      time_rate_reset_btn.y = height - time_sliders_height - time_sliders_gap_y
      time_rate_reset_btn.w = time_sliders_reset_btn_width
      time_rate_reset_btn.h = time_sliders_height
      
      if not time_slider_absolute:
        time_details = get_time_slider_delta_surface()
      time_rate_details = get_time_rate_slider_surface()
  
  recalculate_vars_after_resize()
  
  while loop:
    # update
    
    left_btn.enabled = run_mode.value > 1
    right_btn.enabled = run_mode.value < len(run_modes)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        loop = False
      
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if left_btn.is_pressed(event.pos):
            run_mode = run_modes[run_mode.value - 2]
          elif right_btn.is_pressed(event.pos):
            run_mode = run_modes[run_mode.value]
        
        if time_mode == TimeMode.CUSTOMIZABLE:
          if event.button == 1:
            if time_slider.is_pressed(event.pos):
              time_slider.value = time_slider.get_pressed_value(event.pos)
              reset_time_base_to_current()
              old_time_rate = time_rate
              time_rate = FixedPrec(0)
              old_time_base = time_base
              time_delta = time_norm_to_true_delta(time_slider.value)
              time_base = old_time_base + time_delta
              dragging_time_slider = True
            elif time_rate_slider.is_pressed(event.pos):
              time_rate_slider.value = time_rate_slider.get_pressed_value(event.pos)
              time_rate, time_rate_slider.value = time_rate_norm_to_true(time_rate_slider.value)
              reset_time_base_to_current()
              dragging_time_rate_slider = True
            elif time_reset_btn.is_pressed(event.pos):
              time_reset_time = TimeInstant.now().time
              time_base = time_reset_time
            elif time_rate_reset_btn.is_pressed(event.pos):
              time_rate = FixedPrec(1)
              time_rate_slider.value = time_rate_true_to_norm(time_rate)
              reset_time_base_to_current()
      
      elif event.type == pygame.MOUSEMOTION:
        if time_mode == TimeMode.CUSTOMIZABLE:
          if dragging_time_slider:
            time_slider.value = time_slider.get_pressed_value(event.pos)
            time_delta = time_norm_to_true_delta(time_slider.value)
            time_base = old_time_base + time_delta
          
          if dragging_time_rate_slider:
            time_rate_slider.value = time_rate_slider.get_pressed_value(event.pos)
            time_rate, time_rate_slider.value = time_rate_norm_to_true(time_rate_slider.value)
            reset_time_base_to_current()
      
      elif event.type == pygame.MOUSEBUTTONUP:
        if time_mode == TimeMode.CUSTOMIZABLE:
          if event.button == 1 and (dragging_time_slider or dragging_time_rate_slider):
            dragging_time_slider = False
            dragging_time_rate_slider = False
            time_slider.value = 0.5
            if old_time_rate != None:
              time_rate = old_time_rate
              old_time_rate = None
              time_base = old_time_base + time_delta
              time_reset_time = true_now.time
              old_time_base = None
              time_delta = None
      
      elif event.type == pygame.WINDOWRESIZED:
        width = screen.get_width()
        height = screen.get_height()
        
        recalculate_vars_after_resize()
    
    # draw
    
    screen.fill((0, 0, 0))
    
    left_btn.draw()
    right_btn.draw()
    
    draw_text_centered(screen, run_mode_names[run_mode], (width / 2, 45), horz_align = 0.5, size = 43)
    draw_text_centered(screen, f'{clock.get_fps():.1f} FPS, {clock.get_busy_fraction() * 100:0>4.1f}% use', (90, 45), size = 30)
    
    true_now = TimeInstant.now()
    
    if time_mode == TimeMode.CURRENT:
      now = true_now
    elif time_mode == TimeMode.LEAP_SEC_REPLAY:
      now = TimeInstant(
        (
          true_now.time -
          prgm_start_secs
        ) * 1 +
        TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 50, 0).time
      )
    elif time_mode == TimeMode.CUSTOMIZABLE:
      now = TimeInstant(
        (
          true_now.time -
          time_reset_time
        ) * time_rate +
        time_base
      )
    
    if time_mode == TimeMode.CUSTOMIZABLE:
      if time_slider_absolute:
        draw_time_delta_line_true(screen, 0, (255, 255, 255))
        
        if dragging_time_slider:
          visual_time = TimeInstant(old_time_base)
        else:
          visual_time = now
        
        year, month, day, hour, minute, second, _ = visual_time.to_date_tuple_utc()
        
        old_time_year_exp_start = None
        old_time_year_exp_end = None
        
        for exp in range(floor(log10(10.0 ** time_max_exp / APPROX_SECS_PER_YEAR)), -1, -1):
          time_year_exp_start = TimeInstant.from_date_tuple_utc(year // 10 ** exp * 10 ** exp, 1, 1, 0, 0, 0, 0)
          time_year_exp_end = TimeInstant.from_date_tuple_utc((year // 10 ** exp + 1) * 10 ** exp, 1, 1, 0, 0, 0, 0)
          if 10 ** exp > year and year > 0:
            time_year_exp_start_2 = TimeInstant.from_date_tuple_utc(-10 ** exp, 1, 1, 0, 0, 0, 0)
            draw_time_line_true(time_year_exp_start_2, time_year_exp_start_2.to_format_string_utc('%Y'))
          if -10 ** exp < year and year <= 0:
            time_year_exp_end_2 = TimeInstant.from_date_tuple_utc(10 ** exp, 1, 1, 0, 0, 0, 0)
            draw_time_line_true(time_year_exp_end_2, time_year_exp_end_2.to_format_string_utc('%Y'))
          
          if time_year_exp_start != old_time_year_exp_start:
            draw_time_line_true(time_year_exp_start, time_year_exp_start.to_format_string_utc('%Y'))
          if time_year_exp_end != old_time_year_exp_end:
            draw_time_line_true(time_year_exp_end, time_year_exp_end.to_format_string_utc('%Y'))
          
          old_time_year_exp_start = time_year_exp_start
          old_time_year_exp_end = time_year_exp_end
        
        time_month_start = TimeInstant.from_date_tuple_utc(year, month, 1, 0, 0, 0, 0)
        time_month_end = TimeInstant.from_date_tuple_utc(year, month + 1, 1, 0, 0, 0, 0)
        
        if time_month_start != time_year_exp_start:
          draw_time_line_true(time_month_start, time_month_start.to_format_string_utc('%Y-%m'))
        if time_month_end != time_year_exp_end:
          draw_time_line_true(time_month_end, time_month_end.to_format_string_utc('%Y-%m'))
        
        time_day_start = TimeInstant.from_date_tuple_utc(year, month, day, 0, 0, 0, 0)
        time_halfday = TimeInstant.from_date_tuple_utc(year, month, day, 12, 0, 0, 0)
        time_day_end = TimeInstant.from_date_tuple_utc(year, month, day + 1, 0, 0, 0, 0)
        
        if time_day_start != time_month_start:
          draw_time_line_true(time_day_start, time_day_start.to_format_string_utc('%Y-%m-%d'))
        draw_time_line_true(time_halfday, time_halfday.to_format_string_utc('%H:%M'))
        if time_day_end != time_month_end:
          draw_time_line_true(time_day_end, time_day_end.to_format_string_utc('%Y-%m-%d'))
        
        time_hour_start = TimeInstant.from_date_tuple_utc(year, month, day, hour, 0, 0, 0)
        time_hour_end = TimeInstant.from_date_tuple_utc(year, month, day, hour + 1, 0, 0, 0)
        
        if time_hour_start != time_day_start and time_hour_start != time_halfday:
          draw_time_line_true(time_hour_start, time_hour_start.to_format_string_utc('%H:%M'))
        if time_hour_end != time_day_end and time_hour_end != time_halfday:
          draw_time_line_true(time_hour_end, time_hour_end.to_format_string_utc('%H:%M'))
        
        time_15min_start = TimeInstant.from_date_tuple_utc(year, month, day, hour, minute // 15 * 15, 0, 0)
        time_15min_end = TimeInstant.from_date_tuple_utc(year, month, day, hour, (minute // 15 + 1) * 15, 0, 0)
        
        if time_15min_start != time_hour_start:
          draw_time_line_true(time_15min_start, time_15min_start.to_format_string_utc('%H:%M'))
        if time_15min_end != time_hour_end:
          draw_time_line_true(time_15min_end, time_15min_end.to_format_string_utc('%H:%M'))
        
        time_min_start = TimeInstant.from_date_tuple_utc(year, month, day, hour, minute, 0, 0)
        time_min_end = TimeInstant.from_date_tuple_utc(year, month, day, hour, minute + 1, 0, 0)
        
        if time_min_start != time_15min_start:
          draw_time_line_true(time_min_start, time_min_start.to_format_string_utc('%H:%M'))
        if time_min_end != time_15min_end:
          draw_time_line_true(time_min_end, time_min_end.to_format_string_utc('%H:%M'))
        
        time_15sec_start = TimeInstant.from_date_tuple_utc(year, month, day, hour, minute, second // 15 * 15, 0)
        if second // 15 * 15 == 45:
          time_15sec_end = TimeInstant.from_date_tuple_utc(year, month, day, hour, minute + 1, 0, 0)
        else:
          time_15sec_end = time_15sec_start + TimeDelta(15)
        
        if time_15sec_start != time_min_start:
          draw_time_line_true(time_15sec_start, time_15sec_start.to_format_string_utc('%H:%M:%S'))
        if time_15sec_end != time_min_end:
          draw_time_line_true(time_15sec_end, time_15sec_end.to_format_string_utc('%H:%M:%S'))
        
        time_sec_start = TimeInstant.from_date_tuple_utc(year, month, day, hour, minute, second, 0)
        time_sec_end = time_sec_start + TimeDelta(1)
        
        if time_sec_start != time_15sec_start:
          draw_time_line_true(time_sec_start, time_sec_start.to_format_string_utc('%H:%M:%S'))
        if time_sec_end != time_15sec_end:
          draw_time_line_true(time_sec_end, time_sec_end.to_format_string_utc('%H:%M:%S'))
      else:
        screen.blit(
          time_details,
          time_slider.local_to_world(0, 0, True)
        )
      
      time_slider.draw()
      time_reset_btn.draw()
      
      screen.blit(
        time_rate_details,
        time_rate_slider.local_to_world(0, 0, True)
      )
      
      time_rate_slider.draw()
      time_rate_reset_btn.draw()
      
      if old_time_rate:
        visual_time_rate = old_time_rate
      else:
        visual_time_rate = time_rate
      draw_text_centered(
        screen,
        f'{float(visual_time_rate):.2e}x',
        (
          width - time_rate_text_size / 2 - time_sliders_edge_dist_x,
          height - time_sliders_height / 2 - time_sliders_gap_y + 1
        ),
        horz_align = 0.5,
        size = 23
      )
    
    if run_mode == RunMode.CLOCK:
      ...
    
    elif run_mode == RunMode.TIME_STANDARDS:
      if tz != None:
        draw_text_centered(screen, f'TZ:  {now.to_format_string_tz(tz, time_standards_format_str)}',                                                          (width / 2 - time_standards_x_center_offset, time_standards_y_start + 0 * time_standards_y_step))
      draw_text_centered(screen, f'UTC: {now.to_format_string_utc(time_standards_format_str)}',                                                               (width / 2 - time_standards_x_center_offset, time_standards_y_start + 1 * time_standards_y_step))
      draw_text_centered(screen, f'SUT: {now.to_format_string_smear_utc(smear_plan, time_standards_format_str_cap_offset, True)}',                            (width / 2 - time_standards_x_center_offset, time_standards_y_start + 2 * time_standards_y_step))
      if tz != None:
        draw_text_centered(screen, f'STZ: {now.to_format_string_smear_tz(smear_plan, tz, time_standards_format_str_cap_offset, True)}',                       (width / 2 - time_standards_x_center_offset, time_standards_y_start + 3 * time_standards_y_step))
      draw_text_centered(screen, f'TAI: {now.to_format_string_tai(time_standards_format_str)}',                                                               (width / 2 - time_standards_x_center_offset, time_standards_y_start + 4 * time_standards_y_step))
      draw_text_centered(screen, f'TT:  {now.to_format_string_mono(TimeInstant.TIME_SCALES.TT, time_standards_format_str)}',                                  (width / 2 - time_standards_x_center_offset, time_standards_y_start + 5 * time_standards_y_step))
      draw_text_centered(screen, f'TDB: {now.to_format_string_mono(TimeInstant.TIME_SCALES.TDB, time_standards_format_str_cap_offset)}',                      (width / 2 - time_standards_x_center_offset, time_standards_y_start + 6 * time_standards_y_step))
      draw_text_centered(screen, f'TCG: {now.to_format_string_mono(TimeInstant.TIME_SCALES.TCG, time_standards_format_str_cap_offset)}',                      (width / 2 - time_standards_x_center_offset, time_standards_y_start + 7 * time_standards_y_step))
      draw_text_centered(screen, f'TCB: {now.to_format_string_mono(TimeInstant.TIME_SCALES.TCB, time_standards_format_str_cap_offset)}',                      (width / 2 - time_standards_x_center_offset, time_standards_y_start + 8 * time_standards_y_step))
      draw_text_centered(screen, f'GAL: {now.to_format_string_mono(TimeInstant.TIME_SCALES.GALACTIC_COORDINATE_TIME, time_standards_format_str_cap_offset)}', (width / 2 - time_standards_x_center_offset, time_standards_y_start + 9 * time_standards_y_step))
      draw_text_centered(screen, f'UNI: {now.to_format_string_mono(TimeInstant.TIME_SCALES.UNIVERSE_COORDINATE_TIME, time_standards_format_str_cap_offset)}', (width / 2 - time_standards_x_center_offset, time_standards_y_start + 10 * time_standards_y_step))
      draw_text_centered(screen, f'UT1: {now.to_format_string_mono(TimeInstant.TIME_SCALES.UT1, time_standards_format_str_cap_offset)}',                      (width / 2 - time_standards_x_center_offset, time_standards_y_start + 11 * time_standards_y_step))
      if longitude != None:
        draw_text_centered(screen, f'MST: {now.to_format_string_solar(longitude, False, time_standards_format_str_cap_offset)}',                              (width / 2 - time_standards_x_center_offset, time_standards_y_start + 12 * time_standards_y_step))
        draw_text_centered(screen, f'TST: {now.to_format_string_solar(longitude, True, time_standards_format_str_cap_offset)}',                               (width / 2 - time_standards_x_center_offset, time_standards_y_start + 13 * time_standards_y_step))
    
    elif run_mode == RunMode.CALENDARS:
      draw_text_centered(screen, f'Julian:               {now.to_format_string_utc(calendars_format_str, date_cls = JulianDate)}',            (width / 2 - calendars_x_center_offset, calendars_y_start + 0 * calendars_y_step))
      draw_text_centered(screen, f'Gregorian:            {now.to_format_string_utc(calendars_format_str, date_cls = GregorianDate)}',         (width / 2 - calendars_x_center_offset, calendars_y_start + 1 * calendars_y_step))
      iso_date: IsoWeekDate = now.get_date_object_utc(IsoWeekDate)
      draw_text_centered(screen, f'ISOWeekDate:          {iso_date.to_iso_string()} {now.to_format_string_utc(calendars_time_format_str)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 2 * calendars_y_step))
      draw_text_centered(screen, f'Holocene:             {now.to_format_string_utc(calendars_format_str, date_cls = HoloceneDate)}',          (width / 2 - calendars_x_center_offset, calendars_y_start + 3 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry010:          {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry010)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 4 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry010LeapMonth: {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry010LeapMonth)}',  (width / 2 - calendars_x_center_offset, calendars_y_start + 5 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry454:          {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry454)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 6 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry454LeapMonth: {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry454LeapMonth)}',  (width / 2 - calendars_x_center_offset, calendars_y_start + 7 * calendars_y_step))
    
    elif run_mode == RunMode.BLANK:
      pass
    
    pygame.display.flip()
    await clock.tick_async(refresh_rate)
  
  pygame.quit()

async def runner():
  async with TaskGroup() as tg:
    main_task = tg.create_task(main())
    update_time_db_task = tg.create_task(update_time_databases_loop())
    main_task.add_done_callback(lambda _: update_time_db_task.cancel())

if __name__ == '__main__':
  run(runner())
