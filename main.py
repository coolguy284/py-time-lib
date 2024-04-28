import code, datetime, pprint, os, sys, time
from enum import Enum

from py_time_lib import *
from py_time_lib.update_leap_seconds import *
from py_time_lib.update_timezone_db import *
from py_time_lib.update_timezone_db import _parse_tzdb_get_filtered_lines, _parse_tzdb_get_processed_lines, _parse_tzdb_get_result_dicts, _parse_tzdb_get_tz_dicts

update_time_databases()

RunModes = Enum('RunModes', (
  'TEST_BASIC_DATE',
  'TEST_ISO_WEEK',
  'TEST_AUTO_LEAP_SECONDS',
  'TEST_CALENDARS',
  'TEST_TZDB',
  'GENERATE_TZDB_DUMP',
  'HELP',
  'REPL',
))

mode = RunModes.HELP

if len(sys.argv) > 1:
  run_mode = sys.argv[1]
  try:
    mode = RunModes[run_mode]
  except KeyError:
    raise SystemExit(f'Unrecognized run mode {run_mode}')

def save_tzdb_stage_1_dump():
  os.makedirs(file_relative_path_to_abs('../main_data'), exist_ok = True)
  
  update_stored_tzdb_if_needed()
  
  with open('main_data/tzdb_dump_stage_1.txt', 'w') as f:
    with get_tzdb_stored_file() as tgz_file:
      data = _parse_tzdb_get_filtered_lines(tgz_file)
    
    f.write('\n'.join(data) + '\n')

def save_tzdb_stage_2_dump():
  os.makedirs(file_relative_path_to_abs('../main_data'), exist_ok = True)
  
  update_stored_tzdb_if_needed()
  
  with open('main_data/tzdb_dump_stage_2.txt', 'w') as f:
    with get_tzdb_stored_file() as tgz_file:
      data = _parse_tzdb_get_result_dicts(_parse_tzdb_get_processed_lines(_parse_tzdb_get_filtered_lines(tgz_file)))
    
    f.write(fancy_format(data) + '\n')

def save_tzdb_stage_3_dump():
  os.makedirs(file_relative_path_to_abs('../main_data'), exist_ok = True)
  
  update_stored_tzdb_if_needed()
  
  with open('main_data/tzdb_dump_stage_3.txt', 'w') as f:
    with get_tzdb_stored_file() as tgz_file:
      data = _parse_tzdb_get_tz_dicts(_parse_tzdb_get_result_dicts(_parse_tzdb_get_processed_lines(_parse_tzdb_get_filtered_lines(tgz_file))))
    
    f.write(fancy_format(data) + '\n')

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
    prev_date = (datetime.date(year, 12, 31) + datetime.timedelta(days = 1)).isocalendar()
    next_date = (datetime.date(year, 1, 1) - datetime.timedelta(days = 1)).isocalendar()
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
elif mode == RunModes.GENERATE_TZDB_DUMP:
  print('Stage 1 dump...')
  save_tzdb_stage_1_dump()
  print('Stage 2 dump...')
  save_tzdb_stage_2_dump()
  print('Stage 3 dump...')
  save_tzdb_stage_3_dump()
elif mode == RunModes.HELP:
  print('Available Run Modes:')
  for mode in RunModes.__members__:
    print(mode)
elif mode == RunModes.REPL:
  # https://stackoverflow.com/questions/5597836/embed-create-an-interactive-python-shell-inside-a-python-program/5597918#5597918
  code.interact(local = globals())
