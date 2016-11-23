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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

