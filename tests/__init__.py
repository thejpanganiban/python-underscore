from underscore import Underscore
import types
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

  def test_filter(self):
    my_seq = [1,2,3,4,5]
    self.assertTrue(self._.filter)
    # Test functional-style
    self.assertEqual(self._.filter(my_seq, lambda x: x % 2 == 0), [2,4])
    # Test OOP-style
    self.assertEqual(self._(my_seq).filter(lambda x: x % 2 == 0), [2,4])

  def test_all(self):
    my_seq = [1,2,False,None,True]
    self.assertTrue(self._.all)
    # Test functional-style
    self.assertEqual(self._.all(my_seq), [1,2,True])
    # Test OOP-style
    self.assertEqual(self._(my_seq).all(), [1,2,True])

  def test_generator(self):
    my_seq = [1,2,3,4,5]
    self.assertTrue(self._.generator)
    # Test functional-style if it returns a generator
    self.assertTrue(isinstance(self._.generator(my_seq), types.GeneratorType))
    # Test OOP-style if it returns a generator
    self.assertTrue(isinstance(self._(my_seq).generator(), types.GeneratorType))
    # Test return values
    self.assertEqual([i for i in self._.generator(my_seq)], my_seq)
    self.assertEqual([i for i in self._(my_seq).generator()], my_seq)
    # Test chaining
    self.assertEqual(self._.chain()
        .generator(my_seq)
        .each(lambda x: x + 1)
        .value(), [2,3,4,5,6])

  def test_chaining(self):
    my_seq = [1,2,3,4,5]
    self.assertTrue(self._.chain)
    # Test functional-style
    self.assertEqual(self._
      .chain(my_seq)
      .each(lambda x: x + 1)
      .filter(lambda x: x % 2 == 0)
      .value(), [2,4,6])
    # Test OOP-style
    self.assertEqual(self._(my_seq)
      .chain()
      .each(lambda x: x + 1)
      .filter(lambda x: x % 2 == 0)
      .value(), [2,4,6])


if __name__ == '__main__':
  unittest.main()
