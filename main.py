from code import interact
from datetime import date, timedelta
from enum import Enum
from os import makedirs
from sys import argv as sys_argv

from py_time_lib import *
from py_time_lib.update_leap_seconds import *
from py_time_lib.update_timezone_db import *
from py_time_lib.update_timezone_db import _parse_tzdb_get_filtered_lines, _parse_tzdb_get_processed_lines, _parse_tzdb_get_result_dicts, _parse_tzdb_get_tz_dicts
from py_time_lib.update_ut1 import *
from py_time_lib.data_py.holidays import *
from py_time_lib.data_py.leap_smear_profiles import *

update_time_databases()

RunModes = Enum('RunModes', (
  'TEST_BASIC_DATE',
  'TEST_ISO_WEEK',
  'TEST_AUTO_LEAP_SECONDS',
  'TEST_CALENDARS',
  'TEST_TZDB',
  'TEST_TIME_SCALES',
  'TEST_UT1',
  'TEST_SMEAR_TIME',
  'GENERATE_TZDB_DUMP',
  'GENERATE_UT1_DUMP',
  'HELP',
  'REPL',
))

mode = RunModes.HELP

if len(sys_argv) > 1:
  run_mode = sys_argv[1]
  try:
    mode = RunModes[run_mode]
  except KeyError:
    raise SystemExit(f'Unrecognized run mode {run_mode}')

def create_main_data_dir():
  makedirs(file_relative_path_to_abs('../main_data'), exist_ok = True)

def save_tzdb_stage_1_dump():
  create_main_data_dir()
  
  update_stored_tzdb_if_needed()
  
  with open('main_data/tzdb_dump_stage_1.txt', 'w') as f:
    with get_tzdb_stored_file() as tgz_file:
      data = _parse_tzdb_get_filtered_lines(tgz_file)
    
    f.write('\n'.join(data) + '\n')

def save_tzdb_stage_2_dump():
  create_main_data_dir()
  
  update_stored_tzdb_if_needed()
  
  with open('main_data/tzdb_dump_stage_2.txt', 'w') as f:
    with get_tzdb_stored_file() as tgz_file:
      data = _parse_tzdb_get_result_dicts(_parse_tzdb_get_processed_lines(_parse_tzdb_get_filtered_lines(tgz_file)))
    
    f.write(fancy_format(data) + '\n')

def save_tzdb_stage_3_dump():
  create_main_data_dir()
  
  update_stored_tzdb_if_needed()
  
  with open('main_data/tzdb_dump_stage_3.txt', 'w') as f:
    with get_tzdb_stored_file() as tgz_file:
      data = _parse_tzdb_get_tz_dicts(_parse_tzdb_get_result_dicts(_parse_tzdb_get_processed_lines(_parse_tzdb_get_filtered_lines(tgz_file))))
    
    f.write(fancy_format(data) + '\n')

def save_ut1_historic_dump():
  create_main_data_dir()
  
  with open('main_data/ut1_dump_historic.txt', 'w') as f:
    f.write('\n'.join(f'{ut1entry.secs_since_epoch} {ut1entry.ut1_minus_tai}' for ut1entry in parse_historic_file(eop_historic_get_file())) + '\n')

def save_ut1_recent_dump():
  create_main_data_dir()
  
  with open('main_data/ut1_dump_recent.txt', 'w') as f:
    f.write('\n'.join(f'{ut1entry.secs_since_epoch} {ut1entry.ut1_minus_tai}' for ut1entry in parse_recent_files(eop_recent_get_file())) + '\n')

def save_ut1_daily_dump():
  create_main_data_dir()
  
  with open('main_data/ut1_dump_daily.txt', 'w') as f:
    f.write('\n'.join(f'{ut1entry.secs_since_epoch} {ut1entry.ut1_minus_tai}' for ut1entry in parse_recent_files(eop_daily_get_file())) + '\n')

def save_ut1_full_dump():
  create_main_data_dir()
  
  with open('main_data/ut1_dump_full.txt', 'w') as f:
    f.write('\n'.join(f'{ut1entry.secs_since_epoch} {ut1entry.ut1_minus_tai}' for ut1entry in get_ut1_offsets()) + '\n')

if mode == RunModes.TEST_BASIC_DATE:
  date_to_days_since_epoch = GregorianDate.date_to_days_since_epoch
  
  print(date_to_days_since_epoch(1901, 1, 1) - date_to_days_since_epoch(1900, 1, 1))
  print(date_to_days_since_epoch(2001, 1, 1) - date_to_days_since_epoch(2000, 1, 1))
  print()
  
  print(date_to_days_since_epoch(0, 1, 1))
  print(date_to_days_since_epoch(0, 13, 1))
  print(date_to_days_since_epoch(1, 1, 1))
  print(date_to_days_since_epoch(0, 25, 1))
  print(date_to_days_since_epoch(2, 1, 1))
  print(date_to_days_since_epoch(0, 788 * 12 + 1, 1))
  print(date_to_days_since_epoch(788, 1, 1))
  print()
  
  print(JulianDate.DAYS_IN_YEAR)
  print(GregorianDate.DAYS_IN_YEAR)
  print()
  
  t1 = TimeInstant(FixedPrec(1000))
  t2 = TimeInstant(FixedPrec(1003))
  print(t1)
  print(t2)
  print(t2 - t1)
  print(t1 - t2)
  print()
  
  print(GregorianDate(2024, 3, 26).days_diff_from_julian())
  print(GregorianDate(1900, 3, 1).days_diff_from_julian())
  print(GregorianDate(1900, 2, 28).days_diff_from_julian())
  print()
  
  print(GregorianDate.from_iso_string('2024-03-27'))
  print()
elif mode == RunModes.TEST_ISO_WEEK:
  def print_date_info(year):
    prev_date = (date(year, 12, 31) + timedelta(days = 1)).isocalendar()
    next_date = (date(year, 1, 1) - timedelta(days = 1)).isocalendar()
    print([prev_date, next_date])
  for i in range(2020, 2030):
    print_date_info(i)
elif mode == RunModes.TEST_AUTO_LEAP_SECONDS:
  #print(parse_leap_sec_file(get_leap_sec_stored_file()))
  #print(get_current_ntp_timestamp())
  print(get_leap_sec_data())
  pass
elif mode == RunModes.TEST_CALENDARS:
  print('Julian:')
  print(JulianDate(2024, 4, 13).get_yearly_calendar())
  print()
  
  print('Gregorian:')
  print(GregorianDate(2024, 4, 13).get_yearly_calendar())
  print()
  
  print('Holocene:')
  print(HoloceneDate(12024, 4, 13).get_yearly_calendar())
  print()
elif mode == RunModes.TEST_TZDB:
  print(repr(get_tzdb_data())[:1000])
elif mode == RunModes.TEST_TIME_SCALES:
  # https://docs.astropy.org/en/stable/time/
  from astropy.time import Time
  t1a = TimeInstant.from_date_tuple_tai(1977, 1, 1, 0, 0, 0, 0)
  t2a = TimeInstant.from_date_tuple_tai(2010, 1, 1, 0, 0, 0, 0)
  t3a = TimeInstant.from_date_tuple_tai(2024, 1, 1, 0, 0, 0, 0)
  t1b = Time('1977-01-01 00:00:00', format='iso', scale='tai')
  t2b = Time('2010-01-01 00:00:00', format='iso', scale='tai')
  t3b = Time('2024-01-01 00:00:00', format='iso', scale='tai')
  print(t2a.get_mono_tai_offset(TimeInstant.TIME_SCALES.TCG) - 32.184, (t2b.tcg - t1b.tcg).to_value(format='sec') - (t2b.tai - t1b.tai).to_value(format='sec'))
  print(t3a.get_mono_tai_offset(TimeInstant.TIME_SCALES.TCG) - 32.184, (t3b.tcg - t1b.tcg).to_value(format='sec') - (t3b.tai - t1b.tai).to_value(format='sec'))
  print(t2a.get_mono_tai_offset(TimeInstant.TIME_SCALES.TCB) - 32.184, (t2b.tcb - t1b.tcb).to_value(format='sec') - (t2b.tai - t1b.tai).to_value(format='sec'))
  print(t3a.get_mono_tai_offset(TimeInstant.TIME_SCALES.TCB) - 32.184, (t3b.tcb - t1b.tcb).to_value(format='sec') - (t3b.tai - t1b.tai).to_value(format='sec'))
elif mode == RunModes.TEST_UT1:
  print(get_ut1_offsets())
elif mode == RunModes.TEST_SMEAR_TIME:
  from timeit import timeit
  func = lambda: TimeInstant.from_date_tuple_utc(2016, 12, 31, 23, 59, 59, 0).to_secs_since_epoch_smear_utc(smear_plan)
  smear_plan = NOON_TO_NOON
  t1 = timeit(func, number = 1000) / 1000
  print(t1)
  smear_plan = LeapSmearPlan(
    LeapSmearSingle(
      start_basis = LeapBasis.START,
      secs_before_start_basis = 5,
      end_basis = LeapBasis.END,
      secs_after_end_basis = 5,
      type = SmearType.COSINE
    ),
    ()
  )
  t2 = timeit(func, number = 1000) / 1000
  print(t2, t2 / t1)
  smear_plan = LeapSmearPlan(
    LeapSmearSingle(
      start_basis = LeapBasis.START,
      secs_before_start_basis = 5,
      end_basis = LeapBasis.END,
      secs_after_end_basis = 5,
      type = SmearType.BUMP
    ),
    ()
  )
  t3 = timeit(func, number = 30) / 30
  print(t3, t3 / t2)
elif mode == RunModes.GENERATE_TZDB_DUMP:
  print('TZDB Stage 1 Dump...')
  save_tzdb_stage_1_dump()
  print('TZDB Stage 2 Dump...')
  save_tzdb_stage_2_dump()
  print('TZDB Stage 3 Dump...')
  save_tzdb_stage_3_dump()
elif mode == RunModes.GENERATE_UT1_DUMP:
  print('UT1 Historic Dump...')
  save_ut1_historic_dump()
  print('UT1 Recent Dump...')
  save_ut1_recent_dump()
  print('UT1 Daily Dump...')
  save_ut1_daily_dump()
  print('UT1 Full Dump...')
  save_ut1_full_dump()
elif mode == RunModes.HELP:
  print('Available Run Modes:')
  for mode in RunModes.__members__:
    print(mode)
elif mode == RunModes.REPL:
  from datetime import datetime
  import pprint, time
  if len(sys_argv) >= 3:
    # string arg passed in
    print(eval(sys_argv[2]))
  else:
    # https://stackoverflow.com/questions/5597836/embed-create-an-interactive-python-shell-inside-a-python-program/5597918#5597918
    interact(local = globals())
