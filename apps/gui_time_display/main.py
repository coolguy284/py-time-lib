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
from math import ceil, log10
from sys import argv as sys_argv
import pygame
from py_time_lib import FixedPrec, TimeInstant, JulianDate, GregorianDate, IsoWeekDate, HoloceneDate, Symmetry010, Symmetry010LeapMonth, Symmetry454, Symmetry454LeapMonth
from py_time_lib import TIMEZONES, update_time_databases, update_time_databases_loop
from py_time_lib import LeapBasis, SmearType, LeapSmearSingle, LeapSmearPlan

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
  buttons_from_left_percent = 0.03
  buttons_y_coord = 40
  buttons_size = 40
  time_sliders_edge_dist = 15
  time_rate_text_size = 150
  time_sliders_height = 60
  time_sliders_reset_btn_width = 100
  time_standards_format_str = '%a %b %d %Y %I:%M:%S.%.9f %p %:z'
  time_standards_format_str_cap_offset = '%a %b %d %Y %I:%M:%S.%.9f %p %.10z'
  time_standards_x_center_offset = 600
  time_standards_y_start = 100
  time_standards_y_step = 45
  time_linear_frac = 0.06
  time_min_exp = -5
  time_max_exp = 17.8
  time_rate_center_radius = 0.02
  time_rate_min_exp = -5
  time_rate_max_exp = 6
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
    norm_abs = exponential_to_linear(delta_abs)
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
    x = width * buttons_from_left_percent - buttons_size / 2,
    y = buttons_y_coord - buttons_size / 2,
    w = buttons_size,
    h = buttons_size,
    text = '<',
    size = 40
  )
  right_btn = Button(
    screen = screen,
    x = width * (1 - buttons_from_left_percent) - buttons_size / 2,
    y = buttons_y_coord - buttons_size / 2,
    w = buttons_size,
    h = buttons_size,
    text = '>',
    size = 40
  )
  
  if time_mode == TimeMode.CUSTOMIZABLE:
    time_slider = Slider(
      screen = screen,
      x = time_sliders_edge_dist,
      y = height - time_sliders_height * 2 - 10,
      w = width - time_sliders_reset_btn_width - time_sliders_edge_dist * 2,
      h = time_sliders_height,
      orientation = Slider.Orientation.HORIZONTAL
    )
    time_slider.value = 0.5
    
    time_reset_btn = Button(
      screen = screen,
      x = width - time_sliders_reset_btn_width - time_sliders_edge_dist,
      y = height - time_sliders_height * 2 - 10,
      w = time_sliders_reset_btn_width,
      h = time_sliders_height,
      text = 'Reset',
      size = 35
    )
    time_reset_btn.enabled = True
    
    time_rate_slider = Slider(
      screen = screen,
      x = time_sliders_edge_dist,
      y = height - time_sliders_height,
      w = width - time_sliders_reset_btn_width - time_rate_text_size - time_sliders_edge_dist * 2,
      h = time_sliders_height,
      orientation = Slider.Orientation.HORIZONTAL
    )
    time_rate_slider.value = time_rate_true_to_norm(time_rate)
    
    time_rate_reset_btn = Button(
      screen = screen,
      x = width - time_sliders_reset_btn_width - time_rate_text_size - time_sliders_edge_dist,
      y = height - time_sliders_height,
      w = time_sliders_reset_btn_width,
      h = time_sliders_height,
      text = 'Reset',
      size = 35
    )
    time_rate_reset_btn.enabled = True
    
    def draw_time_rate_line_raw(norm_x, color = (127, 127, 127), width = 1):
      pygame.draw.line(
        screen,
        color,
        time_rate_slider.local_to_world(norm_x, 0, True),
        time_rate_slider.local_to_world(norm_x, 1, True),
        width = width
      )
    
    def draw_time_rate_line(value, color = (127, 127, 127), width = 1):
      draw_time_rate_line_raw(
        time_rate_true_to_norm(value),
        color,
        width
      )
    
    def draw_time_rate_text(value):
      draw_text_centered(
        screen,
        f'{value:g}x',
        time_rate_slider.local_to_world(
          time_rate_true_to_norm(value),
          0.5
        ),
        horz_align = 0.8 if value < 0 else 0,
        size = 10,
        rotation = 90 if value < 0 else -90
      )
  
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
      time_slider.draw()
      time_reset_btn.draw()
      
      draw_time_rate_line(0, (255, 255, 255))
      draw_time_rate_line_raw(0.5 + time_rate_center_radius, (255, 255, 255))
      draw_time_rate_line_raw(0.5 - time_rate_center_radius, (255, 255, 255))
      for i in range(1, 10):
        num = 10 ** time_rate_min_exp * (i / 10)
        draw_time_rate_line(num)
        draw_time_rate_line(-num)
      for exp in range(time_rate_min_exp, ceil(time_rate_max_exp), 1):
        draw_time_rate_line(10 ** exp, (255, 255, 255))
        draw_time_rate_line(-10 ** exp, (255, 255, 255))
        draw_time_rate_text(10 ** exp)
        draw_time_rate_text(-10 ** exp)
        for i in range(2, 10):
          num = 10 ** exp * i
          if log10(num) > time_rate_max_exp:
            break
          draw_time_rate_line(num)
          draw_time_rate_line(-num)
      
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
          width - time_rate_text_size / 2 - time_sliders_edge_dist,
          height - time_sliders_height / 2 + 1
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
