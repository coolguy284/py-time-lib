## py-time-lib to_format_string_* Format Specifiers

(some data sourced from [datetime docs](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes))

| Format Specifier | Origin           | Description |
| ---------------- | ---------------- | ----------- |
| %a               | C89 Standard     | 3-letter capitalized weekday name (ex. Sun). |
| %A               | C89 Standard     | Capitalized full weekday name (ex. Sunday). |
| %b               | C89 Standard     | 3-letter capitalized month name (ex. Jan). |
| %B               | C89 Standard     | Capitalized full month name (ex. January). |
| %c               | C89 Standard     | Locale datetime string (ex. Sun Apr 14 13:02:03 2024) |
| %d               | C89 Standard     | 2-digit day in month (01-31). |
| %f               | C89 Standard     | 6-digit fractional second component (000000-999999). |
| %.&lt;number&gt;f      | py-time-lib      | N-digit fractional second component. |
| %G               | datetime library | ISO Week Date 4+ digit year. |
| %H               | C89 Standard     | Hour number in 24-hour format (00-23). |
| %I               | C89 Standard     | Hour number in 12-hour format (01-12). |
| %j               | C89 Standard     | 3-digit ordinal day of year (Jan 1 = 001, Dec 31 = 365/366). |
| %m               | C89 Standard     | 2-digit month in year (01-12). |
| %M               | C89 Standard     | 2-digit minute in hour (00-59). |
| %p               | C89 Standard     | AM/PM indicator string. |
| %S               | C89 Standard     | 2-digit second in minute (00-60 (60 included due to leap seconds)). |
| %u               | datetime library | 1-digit ISO Week Date day in week (1-7, 1=Monday, 7=Sunday). |
| %U               | C89 Standard     | Week in year (Sunday first day), with days before first Sunday counted as week 0 (00-53). |
| %V               | datetime library | 2-digit ISO Week Date week in year (01-53). |
| %w               | C89 Standard     | 1-digit day in week (0-6, 0=Sunday, 6=Saturday). |
| %W               | C89 Standard     | Week in year (Monday first day), with days before first Monday counted as week 0 (00-53). |
| %x               | C89 Standard     | Locale date string (ex. 04/14/24). |
| %X               | C89 Standard     | Locale time string (ex. 13:02:03). |
| %y               | C89 Standard     | 2-digit year without century (00-99). Calculated as mod(year, 100). |
| %Y               | C89 Standard     | 4+-digit year with century (0000-9999+, -000 to -999+). |
| %z               | C89 Standard     | Timezone offset. "Z" for UTC, +HHMM or -HHMM for offset with minute precision, +HH:MM:SS or -HH:MM:SS for offset with second precision, and +HH:MM:SS.Z... or -HH:MM:SS.Z... for offset with subsecond precision, with as many decimal digits needed to show full offset. |
| %Z               | C89 Standard     | Timezone name. |
| %:z              | datetime library | Timezone offset with colons always. +HH:MM or -HH:MM for offset with minute precision, +HH:MM:SS or -HH:MM:SS for offset with second precision, and +HH:MM:SS.Z... or -HH:MM:SS.Z... for offset with subsecond precision, with as many decimal digits needed to show full offset. |
| %.&lt;number&gt;z      | py-time-lib      | Timezone offset with N-digits of precision. %.0z will truncate subsecond component of offset, and %.Nz will display offset to N-digits of precision. |
| %%               | C89 Standard     | Escape sequence for raw "%" in output. |
