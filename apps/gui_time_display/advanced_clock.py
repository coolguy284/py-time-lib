from asyncio import sleep as asyncio_sleep
from time import perf_counter_ns
from pygame.time import wait

from sample_averager import SampleAverager

class AdvancedClock:
  __slots__ = '_perf_counter_loop_start', '_perf_counter_loop_end', '_past_perf_counter_loop_end', '_frame_times', '_busy_fractions'
  
  def __init__(self):
    self._perf_counter_loop_start = None
    self._perf_counter_loop_end = None
    self._past_perf_counter_loop_end = None
    self._frame_times = SampleAverager(100, 2)
    self._busy_fractions = SampleAverager(100, 2)
  
  def _computation_time_ns(self) -> int:
    self._perf_counter_loop_end = perf_counter_ns()
    
    if self._perf_counter_loop_start == None:
      result = 0
    else:
      result = self._perf_counter_loop_end - self._perf_counter_loop_start
    
    return result
  
  def _computation_time_secs(self) -> float:
    return self._computation_time_ns() / 1_000_000_000
  
  def _tick_internal(self, framerate: int) -> tuple:
    expected_frame_time = 1 / framerate
    current_frame_time = self._computation_time_secs()
    remaining_frame_time = max(0, expected_frame_time - current_frame_time)
    busy_fraction = current_frame_time / expected_frame_time
    if self._past_perf_counter_loop_end != None:
      self._frame_times.new_sample_input((self._perf_counter_loop_end - self._past_perf_counter_loop_end) / 1_000_000_000)
    self._busy_fractions.new_sample_input(busy_fraction)
    self._past_perf_counter_loop_end = self._perf_counter_loop_end
    return remaining_frame_time
  
  def tick(self, framerate: int) -> None:
    remaining_frame_time = self._tick_internal(framerate)
    #time_sleep(remaining_frame_time)
    wait(int(remaining_frame_time * 1000))
    self._perf_counter_loop_start = perf_counter_ns()
  
  async def tick_async(self, framerate: int) -> None:
    remaining_frame_time = self._tick_internal(framerate)
    await asyncio_sleep(remaining_frame_time)
    self._perf_counter_loop_start = perf_counter_ns()
  
  def get_fps(self) -> float:
    avg_frame_time = self._frame_times.get_sample_average()
    if avg_frame_time == 0:
      return float('inf')
    else:
      return 1 / avg_frame_time
  
  def get_busy_fraction(self) -> float:
    return self._busy_fractions.get_sample_average()
