# Copyright 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstract base classes for mir.monads package."""

import abc


class DataConstructor(abc.ABCMeta):

    """Metaclass for Haskell-like data constructors.

    Classes must define an arity class attribute.
    """

    def __new__(meta, name, bases, dct):
        arity = int(dct.pop('arity', 0))
        dict_method = _dict_method(dct)

        @dict_method
        def __new__(cls, *args):
            if len(args) != arity:
                raise TypeError('__new__() takes %d arguments' % (arity,))
            return cls(*args)

        @dict_method
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return super().__eq__(other)
            else:
                return False

        bases = (tuple,)
        return super(DataConstructor, meta).__new__(meta, name, bases, dct)


def _dict_method(dct):
    """Decorator for adding methods to dicts."""
    def decorator(f):
        dct[f.__name__] = f
        return f
    return decorator


class UnaryConstructor(metaclass=DataConstructor):
    """Unary data constructor.

    Very roughly speaking, equivalent to Haskell's:

    data SomeType a = UnaryConstructor a

    """
    arity = 1


class Functor(UnaryConstructor):

    """Functor supertype

    class Functor f where
        fmap :: (a -> b) -> f a -> f b

    As a method, the argument order of fmap() is flipped.
    """

    @abc.abstractmethod
    def fmap(self, f):
        """Map a function over the functor."""
        raise NotImplementedError


class Applicative(Functor):

    """Applicative supertype

    class (Functor f) => Applicative f where
        pure :: a -> f a
        (<*>) :: f (a -> b) -> f a -> f b

    Implemented methods:
    amap -- (<*>)
    """

    @abc.abstractmethod
    def amap(self, other):
        """Apply the applicative to another applicative."""
        raise NotImplementedError


class Monad(Applicative):

    """Monad supertype

    class Monad m where
        (>>=) :: m a -> (a -> m b) -> m b
        (>>) :: m a -> m b -> m b
        return :: a -> m a
        fail :: String -> m a

    Implemented methods:
    bind -- (>>=)
    """

    @abc.abstractmethod
    def bind(self, f):
        """Apply a function to the monad."""
        raise NotImplementedError

    def __rshift__(self, f):
        return self.bind(f)


class Monoid(UnaryConstructor):

    """Monoid supertype"""

    @classmethod
    @abc.abstractmethod
    def identity(cls):
        """Return the identity element for the monoid."""
        raise NotImplementedError

    def __mul__(self, other):
        return self.identity()
