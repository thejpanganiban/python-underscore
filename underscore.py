class UnderscoreObject(object):

  is_chain = False
  methods = [
        'each',
        'filter',
        'chain',
        'all',
      ]

  def __init__(self, value=None, *args, **kwargs):
    self.current_value = value

  def _chain_or_return(self, result):
    if self.is_chain:
      self.current_value = result
      return self
    return result

  def each(self, value=None, func=None):
    self.current_value = self.current_value or value
    func = value if callable(value) else func
    return self._chain_or_return([func(item) for item in self.current_value])

  def filter(self, value=None, func=None):
    self.current_value = self.current_value or value
    func = value if callable(value) else func
    return self._chain_or_return([item for item in self.current_value if func(item)])

  def all(self, value=None):
    self.current_value = self.current_value or value
    return self._chain_or_return([item for item in self.current_value if item])

  def value(self):
    return self.current_value

  def chain(self, value=None):
    if value:
      self.current_value = value
    self.is_chain = True
    return self


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
    def wrapper(*fargs, **fkwargs):
      return getattr(self.klass(*fargs, **fkwargs), method_name)
    return wrapper()

  def __call__(self, *args):
    return self.klass(*args)

  def mixin(self, mixin_dict):
    self.mixins.update(mixin_dict)
    for mixin_name, mixin_func in self.mixins.iteritems():
      setattr(self.klass, mixin_name, staticmethod(mixin_func))
      setattr(self, mixin_name, self._proxy_method(mixin_name))
