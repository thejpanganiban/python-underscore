class UnderscoreObjectMeta(object):
  methods = []


class UnderscoreObject(UnderscoreObjectMeta):

  is_chain = False

  def __init__(self, value=None, *args, **kwargs):
    self.current_value = value

  def _chain_or_return(self, result):
    if self.is_chain:
      self.current_value = result
      return self
    return result

  def method_wrapper(method):
    UnderscoreObjectMeta.methods.append(method.__name__)
    def wrapper(*args, **kwargs):
      # Only prevent when the method is chain
      if method.__name__ == 'chain':
        return method(*args, **kwargs)
      # Apply _chain_or_return method here so that we wouldn't
      # have to mind it when we write methods.
      return args[0]._chain_or_return(method(*args, **kwargs))
    return wrapper

  @method_wrapper
  def each(self, value=None, func=None):
    self.current_value = self.current_value or value
    func = value if callable(value) else func
    return [func(item) for item in self.current_value]

  @method_wrapper
  def filter(self, value=None, func=None):
    self.current_value = self.current_value or value
    func = value if callable(value) else func
    return [item for item in self.current_value if func(item)]

  @method_wrapper
  def all(self, value=None):
    self.current_value = self.current_value or value
    return [item for item in self.current_value if item]

  @method_wrapper
  def chain(self, value=None):
    if value:
      self.current_value = value
    self.is_chain = True
    return self

  @method_wrapper
  def generator(self, value=None):
    self.current_value = self.current_value or value
    for item in self.current_value:
      yield item

  def value(self):
    return self.current_value


class Underscore(object):

  klass = None
  mixins = {}

  def __init__(self, underscore_class=UnderscoreObject):
    self.klass = underscore_class
    self._set_methods(underscore_class)

  def _set_methods(self, underscore_class):
    for method_name in underscore_class.methods:
      setattr(self, method_name, self._proxy_method(method_name))

  def _proxy_method(self, method_name):
    def wrapper(*args, **kwargs):
      return getattr(self.klass(*args, **kwargs), method_name)
    return wrapper()

  def __call__(self, *args):
    return self.klass(*args)

  def mixin(self, mixin_dict):
    self.mixins.update(mixin_dict)
    for mixin_name, mixin_func in self.mixins.iteritems():
      setattr(self.klass, mixin_name, staticmethod(mixin_func))
      setattr(self, mixin_name, self._proxy_method(mixin_name))
