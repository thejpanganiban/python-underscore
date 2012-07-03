class UnderscoreObject(object):

  is_chain = False

  def __init__(self, value=None, *args, **kwargs):
    self.current_value = value

  def each(self, value=None, func=None):
    self.current_value = self.current_value or value
    func = value if callable(value) else func
    result = [func(item) for item in self.current_value]
    if self.is_chain:
      self.current_value = result
      return self
    return result

  def filter(self, value=None, func=None):
    self.current_value = self.current_value or value
    func = value if callable(value) else func
    result = [item for item in self.current_value if func(item)]
    if self.is_chain:
      self.current_value = result
      return self
    return result

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
  methods = [
        'each',
        'filter',
        'chain',
      ]

  def __init__(self, underscore_class=UnderscoreObject):
    self.klass = underscore_class
    self._set_methods()

  def _set_methods(self):
    for method_name in self.methods:
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
