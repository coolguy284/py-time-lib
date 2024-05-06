from unittest import TestCase

from .. import binary_search, binary_search_array_split, binary_search_float, FixedPrec

class TestLibFuncs(TestCase):
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
  
  def test_binary_search_float(self):
    self.assertEqual(binary_search_float(lambda x: x <= 3.14159, 3, 4), 3.14159)
    self.assertEqual(binary_search_float(lambda x: x <= FixedPrec('18237645172386537123.141591236471'), FixedPrec(0), 10 ** 30), FixedPrec('18237645172386537123.141591236471'))
