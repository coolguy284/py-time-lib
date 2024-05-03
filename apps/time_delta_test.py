from pathlib import Path
import os, sys

# https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
# https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
parent_dir = Path(os.path.realpath(__file__)).parent.parent
sys.path.append(str(parent_dir))

from time import sleep, perf_counter_ns, monotonic_ns, time_ns
from py_time_lib import FixedPrec
from py_time_lib.constants import NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX

def format_offsets(delta_time, delta_monotone):
  return (
    f'{f'{FixedPrec(delta_time, NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX)!s}':>12}  ' +
    f'{f'{FixedPrec(delta_monotone, NOMINAL_NANOSECS_PER_SEC_LOG_FIXEDPREC_RADIX)!s}':>12}'
  )

def times():
  delta_time = time_ns() - perf_counter_ns()
  delta_monotone = monotonic_ns() - perf_counter_ns()
  return delta_time, delta_monotone

delta_time_initial, delta_monotone_initial = times()

def times_delta():
  delta_time, delta_monotone = times()
  return format_offsets(delta_time - delta_time_initial, delta_monotone - delta_monotone_initial)

print('Initial offsets:')
print(format_offsets(delta_time_initial, delta_monotone_initial))

while True:
  print(times_delta())
  sleep(1)
