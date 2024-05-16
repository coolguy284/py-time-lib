from random import random, seed

# from https://github.com/coolguy284/c284-webmain-1/blob/main/srv_web_main/websites/public/misc/debug/time_syncer_2/js/sample_averager.js
class SampleAverager:
  __slots__ = '_max_samples', '_samples', '_ignored_start_samples', '_current_sample_index', '_sample_average'
  _max_samples: int
  _ignored_start_samples: int
  _current_sample_index: int
  _samples: list[float]
  _sample_average: float
  
  def __init__(self, max_samples: int, ignored_start_samples: int):
    self._samples = [0]
    self._sample_average = 0
    self._max_samples = max_samples
    self._ignored_start_samples = ignored_start_samples
    self._current_sample_index = -self._ignored_start_samples
  
  def _update_at_index(self, index: int, value: float) -> None:
    self._sample_average -= self._samples[index] / len(self._samples)
    self._samples[index] = value
    self._sample_average += self._samples[index] / len(self._samples)
  
  def _append_to_end(self, value: float) -> None:
    self._sample_average *= len(self._samples) / (len(self._samples) + 1)
    self._samples.append(value)
    self._sample_average += self._samples[-1] / len(self._samples)
  
  def _remove_at_index(self, index: int) -> None:
    self._sample_average -= self._samples[index] / len(self._samples)
    self._sample_average *= len(self._samples) / (len(self._samples) - 1)
    del self._samples[index]
  
  def new_sample_input(self, sample: float) -> None:
    if self._current_sample_index < 0:
      self._current_sample_index += 1
    else:
      if 0 <= self._current_sample_index < len(self._samples):
        self._update_at_index(self._current_sample_index, sample)
      else:
        if len(self._samples) >= self._max_samples:
          self._current_sample_index = 0
          self._update_at_index(self._current_sample_index, sample)
        else:
          self._append_to_end(sample)
      
      self._current_sample_index += 1
  
  def get_sample_average(self) -> float:
    return self._sample_average
  
  def num_samples(self) -> int:
    return len(self._samples)
  
  def max_samples(self) -> int:
    return self._max_samples
  
  def set_max_samples(self, new_max: int) -> None:
    self._max_samples = new_max
    
    while len(self._samples) > self._max_samples:
      self._remove_at_index(0)
      if self._current_sample_index > 0:
        self._current_sample_index -= 1
  
  def clear(self) -> None:
    self._current_sample_index = -self._ignored_start_samples
    self._samples = [0]
  
  def _get_true_average(self) -> float:
    return sum(self._samples) / len(self._samples)
  
  def recalculate(self) -> None:
    self._sample_average = self._get_true_average()

def test_sample_averager() -> None:
  # test 1
  
  seed(42)
  nums1 = [random() for _ in range(258)]
  nums2 = [random() for _ in range(150)]
  
  avg = SampleAverager(100, 1)
  
  def check_integrity():
    reported_avg = avg.get_sample_average()
    true_avg = avg._get_true_average()
    diff = abs(reported_avg - true_avg)
    
    if diff > 1e-14:
      raise AssertionError(f'Integrity check failed: average: reported: {reported_avg}, true: {true_avg}, diff: {diff}')
    
    if avg.num_samples() > avg.max_samples():
      raise AssertionError(f'Integrity check failed: num max samples: current: {avg.num_samples()}, max: {avg.max_samples()}')
  
  def new_input_then_integrity(x):
    avg.new_sample_input(x)
    check_integrity()
  
  for x in nums1:
    new_input_then_integrity(x)
  
  avg.set_max_samples(10)
  check_integrity()
  
  for x in nums2:
    new_input_then_integrity(x)
  
  # test 2
  
  avg = SampleAverager(100, 1)
  avg.new_sample_input(0.2)
  avg.new_sample_input(0.2)
  print(avg.get_sample_average())
  print(avg.get_sample_average())
  avg.new_sample_input(0.2)
  avg.new_sample_input(0.2)
  avg.new_sample_input(0.2)
  avg.new_sample_input(0.2)
  
  avg = SampleAverager(100, 1)
  avg.new_sample_input(4)
  avg.new_sample_input(4)
  print(avg.get_sample_average())
  print(avg.get_sample_average())
  avg.new_sample_input(4)
  avg.new_sample_input(4)
  avg.new_sample_input(4)
  avg.new_sample_input(4)
  
  print('SampleAverager test successful.')
