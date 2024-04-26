from collections import namedtuple

# date tuples

MonthWeekDate = namedtuple('MonthWeekDate', ('year', 'month', 'week', 'day_of_week'))

# time tuples

LeapSecEntry = namedtuple('LeapSecEntry', ('date_str', 'time_in_day_secs', 'leap_sec_delta'))

SecsSinceEpochUTC = namedtuple('SecsSinceEpochUTC', ('secs_since_epoch', 'leap_second_fold'))
SecsSinceEpochTZ = namedtuple('SecsSinceEpochTZ', ('secs_since_epoch', 'dst_second_fold', 'leap_second_fold'))
DateTupleBasic = namedtuple('DateTupleBasic', ('year', 'month', 'day', 'hour', 'minute', 'second', 'frac_second'))
DateTupleTZ = namedtuple('DateTupleTZ', ('year', 'month', 'day', 'hour', 'minute', 'second', 'frac_second', 'dst_second_fold'))

UnixTimestampUTC = namedtuple('SecsSinceEpochUTC', ('unix_secs_since_epoch', 'leap_second_fold'))
