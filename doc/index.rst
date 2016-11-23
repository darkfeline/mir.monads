mir.monads documentation
========================

mir.monads is a simple, but rigorous implementation of monads in
Python.

Monads
------

.. module:: mir.monads.id

Identity
^^^^^^^^

The identity monad is the simplest monad.  It's not particularly
useful, especially in Python, although its :meth:`fmap` method can be
used to emulate Clojure's threading operator.

.. code-block:: python

   def add_one(x):
       return x + 1

   (Identity(1)
    .fmap(add_one)
    .fmap(add_one)
    .fmap(add_one)) == 4

    # This is equivalent to the following
    add_one(add_one(add_one(1))) == 4

.. class:: Identity(v)

   Identity instances are instances of :class:`Monad`, and so support
   all associated methods.

Defining additional monads
--------------------------

.. module:: mir.monads.abc

:mod:`mir.monads.abc`
^^^^^^^^^^^^^^^^^^^^^

This module contains abstract base classes related to monads.  These
define interfaces that correspond to Haskell typeclasses.

.. class:: Functor

   ::

      class Functor f where
          fmap :: (a -> b) -> f a -> f b

   Functors are things that can be mapped over.  Functors have one
   method, :meth:`fmap`.

   .. method:: fmap(f)

      Map a function over the functor.

.. class:: Applicative

   ::

      class (Functor f) => Applicative f where
          pure :: a -> f a
          (<*>) :: f (a -> b) -> f a -> f b

   An Applicative is also a :class:`Functor`.  Applicatives are functors
   that can hold a function that can be applied to other functors of
   the same type.

   Applicatives have an additional method :meth:`apply`, which
   implements ``(<*>)``.

   .. method:: apply(other)

      Apply this applicative to the other applicative.

.. class:: Monad

   ::

      class Monad m where
          (>>=) :: m a -> (a -> m b) -> m b
          (>>) :: m a -> m b -> m b
          return :: a -> m a
          fail :: String -> m a

   A Monad is also an :class:`Applicative`.  Monads will not be
   discussed in depth here, but put simply, monads represent
   sequential computation.

   Monads have a method :meth:`bind`, which implements ``(>>=)``.

   .. method:: bind(f)

      Apply the function to the monad.

.. module:: mir.monads.data

:mod:`mir.monads.data`
^^^^^^^^^^^^^^^^^^^^^^

This module defines a metaclass for data constructors.  Data
constructors are like namedtuples, except that they are strictly
typed.

See the :mod:`mir.monads.maybe` module for an example of how data
constructors are defined.

.. class:: Constructor

   Constructor is a metaclass for data constructors.  Instances of
   Constructor (classes that use Constructor as a metaclass) must
   define an :attr:`arity` class attribute.

   .. attribute:: arity

      The arity of the data constructor (how many arguments it takes).

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

