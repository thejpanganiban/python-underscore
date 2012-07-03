class UnderscoreObject(object):

  current_value = None
  args = None
  kwargs = None
  is_chain = False

  def __init__(self, value=None, is_chain=False, *args, **kwargs):
    if value:
      self.current_value = value

    if is_chain:
      self.is_chain = is_chain

    self.args = args
    self.kwargs = kwargs

  def value(self):
    return self.current_value

  def each(self, func):
    result = [func(item) for item in self.current_value]
    if self.is_chain:
      self.current_value = result
      return self
    return result

  def filter(self, func):
    result = [item for item in self.current_value if func(item)]
    if self.is_chain:
      self.current_value = result
      return self
    return result

  def chain(self):
    self.is_chain = True
    return self


class Underscore(object):

  klass = None
  mixins = {}

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
    self.mixins.update(mixin_dict)
    for mixin_name, mixin_func in self.mixins.iteritems():
      # Used for OOP-Style calls.
      setattr(self.klass, mixin_name, staticmethod(mixin_func))
      # Used for functional-style calls.
      setattr(self, mixin_name, self._proxy_mixin(mixin_name))

  def each(self, value, func):
    return self.klass(value).each(func)

  def filter(self, value, func):
    return self.klass(value).filter(func)

  def chain(self, value):
    return self.klass(value, is_chain=True)
