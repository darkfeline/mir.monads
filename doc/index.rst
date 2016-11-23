mir.monads documentation
========================

mir.monads is a simple, but rigorous implementation of monads and
other functional concepts in Python.

.. module:: mir.monads.abc

:mod:`mir.monads.abc`
---------------------

This module contains abstract base classes related to monads.  These define interfaces that correspond to Haskell typeclasses.

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

