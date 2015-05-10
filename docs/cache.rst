Caching functions with :py:func:`vlermv.cache`
==================================================
A function receives input, does something, and then returns output.

If you decorate a function :py:func:`~vlermv.cache`, the inputs and
outputs get recorded;
if you call the function again with the same input, it returns the
output from the cache instead of doing what it would normally do.

I'll discuss how the cache works, give an example of the simplest
way you can use it, and then show you other ways you can use it.

How it works
~~~~~~~~~~~~~~~~~
:py:func:`~vlermv.cache` is a function that returns a decorator.
That is, it is a function that returns a function that takes a
function and returns yet another function.

.. autofunction:: vlermv.cache

Simplest usage
~~~~~~~~~~~~~~~~~~
Decorate your function with :py:func:`~vlermv.cache`, passing it no
arguments. ::

    @vlermv.cache()
    def is_prime(number):
        for n in range(2, number):
            if number % n == 0:
                return False
        return True

Now you can call :py:func:`is_prime` as if it's a normal function, and
if you call it twice, the second call will load from the cache.

Non-default directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you pass no arguments to cache, as in the example above,
the cache will be stored in a directory named after the function.
To set a different directory, pass it as an argument. ::

    @vlermv.cache('~/.primes')
    def is_prime(number):
        for n in range(2, number):
            if number % n == 0:
                return False
        return True

I recommend storing your caches in dotted directories under your
home directory, as you see above.

Non-identifying arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to pass an argument but not use it as an identifier,
pass a non-keyword argument; those get passed along to the function
but don't form the identifier. For example, ::

    @vlermv.cache('~/.http')
    def get(url, auth = None):
        return requests.get(url, auth = auth)

    get('http://this.website.com', auth = ('username', 'password'))

Refreshing the cache
~~~~~~~~~~~~~~~~~~~~~~~~~~
I find that I sometimes want to refresh the cache for a particular
file, only. This is usually because an error occurred and I have fixed
the error. You can delete the cache like this. ::

    @vlermv.cache(key_transformer = vlermv.transformers.magic)
    def is_prime(number):
        for n in range(2, number):
            if number % n == 0:
                return False
        return True

    is_prime(100)
    del(is_prime[100])

The cache is an instance of :py:class:`~vlermv.Vlermv`.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The above method for refreshing the cache works because :py:func:`is_prime`
isn't really a function; it is in fact a :py:class:`~vlermv.Vlermv` object,
and Vlermv has a special :py:meth:`~object.__call__` method.

Thus, you can use it in all of the ways that you can use
:py:class:`~vlermv.Vlermv`. ::

    @vlermv.cache(key_transformer = vlermv.transformers.magic)
    def f(x, y):
        return x + y

    print(f(3,4))
    # 7

    print(list(f.keys()))
    # [('3', '4')]

You can even set the value to be something weird. ::

    f[('a', 8)] = None, {'key':'value'}
    print(f('a', 8))
    # 0

Each value in :py:obj:`f` is a tuple of the error and the returned value.
At least one of these is always :py:const:`None`.
If the error is :py:const:`None`, the decorated function returns the
the value; otherwise, the error is raised. (And the value is :py:const:`None`
because the function never returned.)

Vlermv configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The kwargs get passed to :py:class:`~vlermv.Vlermv`, so you
can do fun things like changing the serialization function. ::

    @vlermv.cache('~/.http', serializer = vlermv.serializers.identity_str)
    def get(url):
        return requests.get(url).text

Decorating a function that takes no arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I have discussed how you can use the :py:func:`~vlermv.cache` decorator
when your function takes arguments. Sometimes your function doesn't take
any arguments; if you naively try something like this, you'll get an error. ::

    @vlermv.cache()
    def take_picture():
        return my_webcam.take_picture()

This happens because :py:func:`~vlermv.Vlermv` doesn't have anything to
form a key from; all it has is an empty :py:class:`tuple`.

If your function doesn't take any arguments but you want to cache it,
then it probably falls into one of the following two categories.

1. It truly doesn't take any arguments, but it takes a very long time
   to run.
2. It truly does take arguments, but you haven't made the arguments
   explicit.

No arguments
^^^^^^^^^^^^^^^^^
If the function will always return the same result no matter how many
times you run it, then it's kind of a constant. If I had to guess,
I would say that you made it a function rather than just a value because
it takes a very long time to run.

In this case, you might not really need Vlermv, as you are just storing
one value. The :py:class:`dictionary interface <vlermv.Vlermv>` might make
your code a bit more legible than the decorator interface. ::

    v = vlermv.Vlermv('results')
    v['picture'] = take_picture()

Alternatively, you might break apart your function into more parts and
apply caches to the parts that do take arguments.

Yes arguments
^^^^^^^^^^^^^^^^^^^
If your function isn't just a constant that takes a long time to compute,
then your function really does take arguments. There are two situations I
will discuss.

1. Implicit arguments are set as global variables or hard-coded names.
   (Less likely but easier to explain)
2. The implicit argument is the entire state of the world, or the present date.

Here's an example of the first one. ::

    @cache()
    def get_widgets():
        return list(database.execute("SELECT * from widgets where country = 'NL';"))

In this instance, we could move the country (:samp:`NL`) to be an argument. ::

    @cache()
    def get_widgets(country):
        return list(database.execute("SELECT * from widgets where country = '?';", country))

As I said above, this hard-coded country issue is probably **not** your issue;
I'm mostly describing it for completeness. This is probably the situation if
you are frequently editing your code to change the country between "NL" and
something else.

**Most likely**, the implicit argument is the entire state of the world, or
the present date. This situation is discussed in the section on
:ref:`archiving <archive>`.
