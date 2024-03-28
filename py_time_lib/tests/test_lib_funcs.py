import unittest

from ..lib_funcs import binary_search, binary_search_array_split

class TestLibFuncs(unittest.TestCase):
  def test_binary_search(self):
    array = [0, 1, 8, 13, 26, 33, 44, 55, 66, 77, 145, 1001]
    self.assertEqual(binary_search(lambda x: array[x] <= -1, 0, len(array)), array.index(0))
    self.assertEqual(binary_search(lambda x: array[x] <= 0, 0, len(array)), array.index(0))
    self.assertEqual(binary_search(lambda x: array[x] <= 44, 0, len(array)), array.index(44))
    self.assertEqual(binary_search(lambda x: array[x] <= 1001, 0, len(array)), array.index(1001))
  
  def test_binary_search_array_split(self):
    array = [0, 1, 8, 13, 26, 33, 44, 55, 66, 77, 145, 1001]
    self.assertEqual(binary_search_array_split(array, lambda x: x <= -1), ([], [0, 1, 8, 13, 26, 33, 44, 55, 66, 77, 145, 1001]))
    self.assertEqual(binary_search_array_split(array, lambda x: x <= 0), ([0], [1, 8, 13, 26, 33, 44, 55, 66, 77, 145, 1001]))
    self.assertEqual(binary_search_array_split(array, lambda x: x <= 44), ([0, 1, 8, 13, 26, 33, 44], [55, 66, 77, 145, 1001]))
    self.assertEqual(binary_search_array_split(array, lambda x: x <= 1001), ([0, 1, 8, 13, 26, 33, 44, 55, 66, 77, 145, 1001], []))
