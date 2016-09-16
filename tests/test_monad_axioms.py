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

import pytest

from mir.monads.base import compose
from mir.monads.id import monadic
from mir.monads.id import unit


@monadic
def add_one(a):
    return a + 1


@monadic
def times_two(a):
    return a * 2


@monadic
def power_three(a):
    return a ** 3


@pytest.mark.parametrize('unit,g,a', [
    (unit, add_one, 1),
])
def test_left_identity(unit, g, a):
    """return >=> g ≡ g"""
    assert compose(unit, g)(a) == g(a)


@pytest.mark.parametrize('f,unit,a', [
    (add_one, unit, 1),
])
def test_right_identity(f, unit, a):
    """f >=> return ≡ f"""
    assert compose(f, unit)(a) == f(a)


@pytest.mark.parametrize('f,g,h,a', [
    (add_one, times_two, power_three, 1),
])
def test_associativity(f, g, h, a):
    """(f >=> g) >=> h ≡ f >=> (g >=> h)"""
    assert compose(compose(f, g), h)(a) \
        == compose(f, compose(g, h))(a)


@pytest.mark.parametrize('unit,f,a', [
    (unit, add_one, 1),
])
def test_bind_left_identity(unit, f, a):
    """return a >>= f ≡ f a"""
    assert unit(a).bind(f) == f(a)


@pytest.mark.parametrize('m,unit', [
    (unit(1), unit),
])
def test_bind_right_identity(m, unit):
    """m >>= return ≡ m"""
    assert m.bind(unit) == m


@pytest.mark.parametrize('m,f,g', [
    (unit(1), add_one, times_two),
])
def test_bind_associativity(m, f, g):
    r"""(m >>= f) >>= g ≡ m >>= (\x -> f x >>= g)"""
    assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))
