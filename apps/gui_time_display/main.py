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
from sys import argv as sys_argv
import pygame
from py_time_lib import FixedPrec, TimeInstant, JulianDate, GregorianDate, IsoWeekDate, HoloceneDate, Symmetry010, Symmetry010LeapMonth, Symmetry454, Symmetry454LeapMonth
from py_time_lib import TIMEZONES, update_time_databases, update_time_databases_loop
from py_time_lib import LeapBasis, SmearType, LeapSmearSingle, LeapSmearPlan

from draw_lib import draw_text_centered
from advanced_clock import AdvancedClock

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
  height = 800
  buttons_from_left_percent = 0.03
  buttons_y_coord = 40
  buttons_size = 40
  button_disabled_color = 127, 127, 127
  button_active_color = 255, 255, 255
  time_standards_format_str = '%a %b %d %Y %I:%M:%S.%.9f %p %:z'
  time_standards_format_str_cap_offset = '%a %b %d %Y %I:%M:%S.%.9f %p %.10z'
  time_standards_x_center_offset = 600
  time_standards_y_start = 100
  time_standards_y_step = 50
  calendars_format_str = '%a %b %d %Y %I:%M:%S.%.9f %p'
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
  ))
  time_mode = TimeMode.CURRENT
  RunMode = Enum('RunMode', (
    'TIME_STANDARDS',
    'CALENDARS',
  ))
  run_modes = list(RunMode)
  run_mode_names = {
    RunMode.TIME_STANDARDS: 'Time Standards',
    RunMode.CALENDARS: 'Calendars (UTC)',
  }
  run_mode = RunMode.TIME_STANDARDS
  
  # https://stackoverflow.com/questions/11603222/allowing-resizing-window-pygame
  screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
  # https://stackoverflow.com/questions/40566585/how-to-change-the-name-of-a-pygame-window/40595418#40595418
  pygame.display.set_caption('GUI Time Display')
  refresh_rate = pygame.display.get_current_refresh_rate()
  clock = AdvancedClock()
  
  loop = True
  
  if time_mode == TimeMode.LEAP_SEC_REPLAY:
    prgm_start_secs = TimeInstant.now().time
  
  while loop:
    left_disabled = run_mode.value <= 1
    right_disabled = run_mode.value >= len(run_modes)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        loop = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if width * buttons_from_left_percent - buttons_size / 2 < event.pos[0] < width * buttons_from_left_percent + buttons_size / 2 and \
            buttons_y_coord - buttons_size / 2 < event.pos[1] < buttons_y_coord + buttons_size / 2:
            if not left_disabled:
              run_mode = run_modes[run_mode.value - 2]
          elif width - width * buttons_from_left_percent - buttons_size / 2 < event.pos[0] < width - width * buttons_from_left_percent + buttons_size / 2 and \
            buttons_y_coord - buttons_size / 2 < event.pos[1] < buttons_y_coord + buttons_size / 2:
            if not right_disabled:
              run_mode = run_modes[run_mode.value]
    
    screen.fill((0, 0, 0))
    
    if time_mode == TimeMode.CURRENT:
      now = TimeInstant.now()
    elif time_mode == TimeMode.LEAP_SEC_REPLAY:
      now = TimeInstant(
        (
          TimeInstant.now().time -
          prgm_start_secs
        ) * 1 +
        TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 50, 0).time
      )
    
    draw_text_centered(
      screen,
      '<',
      (width * buttons_from_left_percent, buttons_y_coord + 5),
      horz_align = 0.5,
      color = button_active_color if not left_disabled else button_disabled_color
    )
    pygame.draw.rect(
      screen,
      button_active_color if not left_disabled else button_disabled_color,
      (width * buttons_from_left_percent - 20, buttons_y_coord - 20, buttons_size, buttons_size),
      width = 2,
      border_top_left_radius = 2,
      border_top_right_radius = 2,
      border_bottom_left_radius = 2,
      border_bottom_right_radius = 2
    )
    
    draw_text_centered(
      screen,
      '>',
      (width - width * buttons_from_left_percent, buttons_y_coord + 5),
      horz_align = 0.5,
      color = button_active_color if not right_disabled else button_disabled_color
    )
    pygame.draw.rect(
      screen,
      button_active_color if not right_disabled else button_disabled_color,
      (width - width * buttons_from_left_percent - 20, buttons_y_coord - 20, buttons_size, buttons_size),
      width = 2,
      border_top_left_radius = 2,
      border_top_right_radius = 2,
      border_bottom_left_radius = 2,
      border_bottom_right_radius = 2
    )
    
    draw_text_centered(screen, run_mode_names[run_mode], (width / 2, 45), horz_align = 0.5, size = 43)
    draw_text_centered(screen, f'{clock.get_fps():.1f} FPS, {clock.get_busy_fraction() * 100:0>4.1f}% use', (90, 45), size = 30)
    
    if run_mode == RunMode.TIME_STANDARDS:
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
      draw_text_centered(screen, f'Holocene:             {now.to_format_string_utc(calendars_format_str, date_cls = HoloceneDate)}',          (width / 2 - calendars_x_center_offset, calendars_y_start + 3 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry010:          {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry010)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 4 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry010LeapMonth: {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry010LeapMonth)}',  (width / 2 - calendars_x_center_offset, calendars_y_start + 5 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry454:          {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry454)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 6 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry454LeapMonth: {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry454LeapMonth)}',  (width / 2 - calendars_x_center_offset, calendars_y_start + 7 * calendars_y_step))
    
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
