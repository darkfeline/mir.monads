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

import functools

from mir.monads.base import Monad
from mir.monads.base import MonadicMonad
from mir.monads.base import NiladicMonad


class Maybe(Monad): pass


class Just(MonadicMonad, Maybe): pass


class Nothing(NiladicMonad, Maybe): pass


def monadic(f):
    @functools.wraps(f)
    def wrapped(a):
        try:
            b = f(a)
        except Exception:
            b = None
        if b is None:
            return Nothing()
        else:
            return Just(b)
    return wrapped


@monadic
def unit(a):
    return a
