from enum import Enum

TimeMode = Enum('TimeMode', (
  'CURRENT',
  'LEAP_SEC_REPLAY',
  'CUSTOMIZABLE',
))

Page = Enum('Page', (
  'CLOCK',
  'TIME_STANDARDS',
  'CALENDARS',
  'BLANK',
))
page_names = {
  Page.CLOCK: 'Clock',
  Page.TIME_STANDARDS: 'Time Standards',
  Page.CALENDARS: 'Calendars (UTC)',
  Page.BLANK: 'Blank',
}
pages = list(Page)

LineStyles = Enum('LineStyles', (
  'THIN',
  'THICK',
  'ORANGE',
  'GREEN',
))
