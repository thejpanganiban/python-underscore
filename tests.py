from underscore import Underscore
import unittest


class UnderscoreTestCase(unittest.TestCase):

  def setUp(self):
    self._ = Underscore()

  def tearDown(self):
    self._ = None

  def test_mixins(self):

    def test_method(x, y):
      return x + y

    self._.mixin({
        'test_method': test_method
      })
    self.assertTrue(self._.test_method)
    self.assertEqual(self._.test_method(5, 4), 9)

  def test_each(self):
    my_seq = [1,2,3,4,5]
    self.assertTrue(self._.each)
    # Test functional-style
    self.assertEqual(self._.each(my_seq, lambda x: x + 1), [2,3,4,5,6])
    # Test OOP-style
    self.assertEqual(self._(my_seq).each(lambda x: x + 2), [3,4,5,6,7])


if __name__ == '__main__':
  unittest.main()
