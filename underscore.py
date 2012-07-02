import itertools
import collections


class UnderscoreObject(object):

  seq = []
  args = None
  kwargs = None

  def __init__(self, *args, **kwargs):
    # Get our sequence
    if isinstance(args[0], collections.Iterable):
      self.seq = args[0]

    self.args = args
    self.kwargs = kwargs

  def each(self, func):
    return [func(item) for item in self.seq]


class Underscore(object):

  klass = None
  mixins = {}

  # We can
  def __init__(self, underscore_class=UnderscoreObject):
    self.klass = underscore_class

  # OOP-Style calls
  def __call__(self, *args):
    return self.klass(*args)

  def _proxy_mixin(self, mixin_name):
    def mixin_func(*args, **kwargs):
      # We're also passing the args and kwargs in the klass object instance for
      # later use. (or so that it could be accessed by the function inside)
      return getattr(self.klass(*args, **kwargs), mixin_name)(*args, **kwargs)
    return mixin_func

  def mixin(self, mixin_dict):
    """Mixin
    """
    self.mixins.update(mixin_dict)
    for mixin_name, mixin_func in self.mixins.iteritems():
      # XXX: Mixin methods will have to have the explicit 'self' as its first
      # argument as we're setting it as a bound method in our klass.
      # Pros would be that the user can access the UnderscoreObject's other
      # methods thru self.
      # Used for OOP-Style calls.
      setattr(self.klass, mixin_name, mixin_func)
      # Used for functional-style calls.
      setattr(self, mixin_name, self._proxy_mixin(mixin_name))

  def each(self, seq, func):
    return self.klass(seq).each(func)
