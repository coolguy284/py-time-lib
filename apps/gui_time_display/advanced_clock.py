from asyncio import sleep as asyncio_sleep
from time import perf_counter_ns, sleep as time_sleep

from sample_averager import SampleAverager

class AdvancedClock:
  __slots__ = '_last_perf_counter_val', '_frame_times', '_busy_fractions'
  
  def __init__(self):
    self._last_perf_counter_val = None
    self._frame_times = SampleAverager(100, 2)
    self._busy_fractions = SampleAverager(100, 2)
  
  def _ns_since_last_call_to_this(self) -> int:
    current_perf_counter = perf_counter_ns()
    
    if self._last_perf_counter_val == None:
      result = 0
    else:
      result = current_perf_counter - self._last_perf_counter_val
    
    self._last_perf_counter_val = current_perf_counter
    
    return result
  
  def _secs_since_last_call_to_this(self) -> float:
    return self._ns_since_last_call_to_this() / 1_000_000_000
  
  def _tick_internal(self, framerate: int) -> tuple:
    expected_frame_time = 1 / framerate
    current_frame_time = self._secs_since_last_call_to_this()
    remaining_frame_time = max(0, expected_frame_time - current_frame_time)
    busy_fraction = current_frame_time / expected_frame_time
    self._frame_times.new_sample_input(current_frame_time + remaining_frame_time)
    self._busy_fractions.new_sample_input(busy_fraction)
    return remaining_frame_time
  
  def tick(self, framerate: int) -> None:
    remaining_frame_time = self._tick_internal(framerate)
    time_sleep(remaining_frame_time)
  
  async def async_tick(self, framerate: int) -> None:
    remaining_frame_time = self._tick_internal(framerate)
    await asyncio_sleep(remaining_frame_time)
  
  def get_fps(self) -> float:
    avg_frame_time = self._frame_times.get_sample_average()
    if avg_frame_time == 0:
      return float('inf')
    else:
      return 1 / avg_frame_time
  
  def get_busy_fraction(self) -> float:
    return self._busy_fractions.get_sample_average()
