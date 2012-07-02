Python Underscore
=================

A python port of [Underscore.js][underscore].

Current Status
--------------

Unfinished.

How to Use
----------

    from underscore import Underscore
    _ = Underscore()

    # functional style
    _.each([1,2,3,4,5], lambda x: return x + 1)

    # object-oriented style
    _([1,2,3,4,5,6]).each(lambda x: return x + 1)


Methods
-------

It's currently under development and you can contribute.

###each

A method for iterating through a sequence.

    _.each(sequence, function)

    _.each([1,2,3,4,5], lambda x: x + 1)
    > [2,3,4,5,6]
    
###mixin

A method for extending the underscore object

    mixin(<dictionary_of_methods>)

A method for extending underscore.

    def util_method(x, y):
      return x + y

    _.mixin({
      'my_method': util_method
    })

    _.my_method(1,2)
    > 3

###filter

A method for filtering items from the list

    _.filter(sequence, function)

    _.filter([1,2,3,4,5], lambda x: x % 2 == 0)
    > [2,4]

###chain

A method for chaining methods. (Wrap with parens to enable multi-lines)

    _.chain(value)...
    _(value).chain()

    (_.chain([1,2,3,4,5])
      .each(lambda x: x + 1)
      .filter(lambda x: x % 2 == 0)
      .value())
    > [2,4,6]

###value

Method for returning the value. (Used when chaining)



Contributing
------------

Just fork the project and submit a pull request.

It is best to write a test for each feature.


Author
------

You can contact me via my email: [me@jpanganiban.com][mail]
or on twitter: [@jpanganiban][twitter]


[underscore]: http://underscorejs.org/
[mail]: mailto:me@jpanganiban.com
[twitter]: http://www.twitter.com/jpanganiban
