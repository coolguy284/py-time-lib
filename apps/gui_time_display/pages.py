from math import cos, sin, pi
from pygame import Surface
from pygame.draw import circle, line
from py_time_lib import FixedPrec, TimeInstant, TimeZone
from py_time_lib import JulianDate, GregorianDate, IsoWeekDate, HoloceneDate, Symmetry010, Symmetry010LeapMonth, Symmetry454, Symmetry454LeapMonth

from constants import Page, get_current_page
from constants import smear_plan
from constants import time_standards_format_str, time_standards_format_str_cap_offset, time_standards_x_center_offset, time_standards_y_start, time_standards_y_step
from constants import calendars_time_format_str, calendars_format_str, calendars_x_center_offset, calendars_y_start, calendars_y_step
from constants import clock_format_str
from lib_draw import draw_text_centered, thick_aaline

def draw_page(screen: Surface, now: TimeInstant, tz: TimeZone, longitude: FixedPrec, central_start_y, central_size):
  width = screen.get_width()
  height = screen.get_height()
  
  match get_current_page():
    case Page.CLOCK:
      if tz != None:
        _, _2, _3, hour, minute, second_int, frac_second, _ = now.to_date_tuple_tz(tz)
        second = second_int + frac_second
        circle(
          screen,
          (255, 255, 255),
          (width * 0.25, central_start_y + central_size / 2 - 20),
          height * 0.3,
          width = 10
        )
        sec_angle = pi / 2 - second / 60 * pi * 2
        thick_aaline(
          screen,
          (width * 0.25, central_start_y + central_size / 2 - 20),
          (width * 0.25 + cos(sec_angle) * height * 0.24, central_start_y + central_size / 2 - 20 - sin(sec_angle) * height * 0.24),
          (255, 0, 0),
          width = 4
        )
        
        date, time = now.to_format_string_tz(tz, clock_format_str).split(' | ')
        draw_text_centered(
          screen,
          f'{date}          {time}',
          (width / 2, central_start_y + central_size - 30),
          horz_align = 0.5
        )
    
    case Page.TIME_STANDARDS:
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
    
    case Page.CALENDARS:
      draw_text_centered(screen, f'Julian:               {now.to_format_string_utc(calendars_format_str, date_cls = JulianDate)}',            (width / 2 - calendars_x_center_offset, calendars_y_start + 0 * calendars_y_step))
      draw_text_centered(screen, f'Gregorian:            {now.to_format_string_utc(calendars_format_str, date_cls = GregorianDate)}',         (width / 2 - calendars_x_center_offset, calendars_y_start + 1 * calendars_y_step))
      iso_date: IsoWeekDate = now.get_date_object_utc(IsoWeekDate)
      draw_text_centered(screen, f'ISOWeekDate:          {iso_date.to_iso_string()} {now.to_format_string_utc(calendars_time_format_str)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 2 * calendars_y_step))
      draw_text_centered(screen, f'Holocene:             {now.to_format_string_utc(calendars_format_str, date_cls = HoloceneDate)}',          (width / 2 - calendars_x_center_offset, calendars_y_start + 3 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry010:          {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry010)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 4 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry010LeapMonth: {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry010LeapMonth)}',  (width / 2 - calendars_x_center_offset, calendars_y_start + 5 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry454:          {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry454)}',           (width / 2 - calendars_x_center_offset, calendars_y_start + 6 * calendars_y_step))
      draw_text_centered(screen, f'Symmetry454LeapMonth: {now.to_format_string_utc(calendars_format_str, date_cls = Symmetry454LeapMonth)}',  (width / 2 - calendars_x_center_offset, calendars_y_start + 7 * calendars_y_step))
    
    case Page.BLANK:
      pass
