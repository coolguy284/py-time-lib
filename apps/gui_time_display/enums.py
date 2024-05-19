from enum import Enum

TimeMode = Enum('TimeMode', (
  'CURRENT',
  'LEAP_SEC_REPLAY',
  'CUSTOMIZABLE',
))

RunMode = Enum('RunMode', (
  'CLOCK',
  'TIME_STANDARDS',
  'CALENDARS',
  'BLANK',
))
run_mode_names = {
  RunMode.CLOCK: 'Clock',
  RunMode.TIME_STANDARDS: 'Time Standards',
  RunMode.CALENDARS: 'Calendars (UTC)',
  RunMode.BLANK: 'Blank',
}
run_modes = list(RunMode)

LineStyles = Enum('LineStyles', (
  'THIN',
  'THICK',
  'ORANGE',
  'GREEN',
))
