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
import inspect


class DataConstructor(abc.ABCMeta):

    """Metaclass for Haskell-like data constructors.

    Classes must define an arity class attribute.

    Very roughly speaking, equivalent to Haskell's:

        data SomeType a = SomeValue a

    Note that the hypothetical type cunstructor may take more arguments than
    the data constructor:

        data SomeType a = SomeValue
        data SomeType a b = SomeValue
        data SomeType a b = SomeValue a
        data SomeType a b c = SomeValue a
    """

    def __new__(meta, name, bases, dct):
        arity = int(dct.pop('arity'))
        dict_method = _dict_method(dct)

        @dict_method
        def __new__(cls, *values):
            if len(values) != arity:
                raise TypeError('__new__() takes %d arguments' % (arity,))
            return tuple.__new__(cls, values)

        @dict_method
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return super(type(self), self).__eq__(other)
            else:
                return False

        bases = (tuple,)
        return super(DataConstructor, meta).__new__(meta, name, bases, dct)


def _dict_method(dct):
    """Decorator for adding methods to a dict."""
    def decorator(f):
        dct[f.__name__] = f
        return f
    return decorator


class Functor(abc.ABC):

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
    apply -- (<*>)
    """

    @abc.abstractmethod
    def apply(self, other):
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


class curry:

    """Decorator to enable currying for a function.

    Calling a curry-able function will either return a partial function or call
    the function and return its result.  The function will only be called if it
    has no unbound parameters.

    Currying a function with keyword-only parameters is an error.

    Parameters with default values are required to be bound when currying.
    """

    def __init__(self, func, args=()):
        self.func = func
        self.args = args

    def __repr__(self):
       return '{cls}({this.func!r}, {this.args!r})'.format(
           cls=type(self).__qualname__,
           this=self)

    def __call__(self, *args):
        func = self.func
        new_args = self.args + args
        if _is_fully_bound(func, new_args):
            return func(*new_args)
        else:
            return curry(self.func, new_args)

    def __mul__(self, other):
        return composition(self, other)


def _is_fully_bound(f, args):
    """Return True if the given arguments bind all of the function's parameters."""
    sig = inspect.signature(f)
    bound_args = sig.bind_partial(*args)
    return len(sig.parameters) == len(bound_args.arguments)


class composition:

    """Composed functions"""

    def __init__(self, a, b):
        assert callable(a), 'Cannot compose non-callable %r' % (a,)
        assert callable(b), 'Cannot compose non-callable %r' % (b,)
        self._a = a
        self._b = b

    def __repr__(self):
        return '{cls}({this._a!r}, {this._b!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, *args, **kwargs):
        return self._a(self._b(*args, **kwargs))


@curry
def kleisli_compose(f: Monad, g: Monad, h):
    """Kleisli composition operator

    Denoted >=> in Haskell.
    """
    return f(h).bind(g)
