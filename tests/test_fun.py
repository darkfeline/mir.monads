# Copyright (C) 2016 Allen Li
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

"""Tests for mir.monads.fun module."""

import mir.monads.fun as fun


def test_curryable_repr():
    got = repr(fun.curryable(lambda: 1))  # pragma: no branch
    assert got.startswith('curryable(')


def test_currying_when_unbound_params():
    function = fun.curryable(lambda a, b: 1)  # pragma: no branch
    got = function(1)
    assert callable(got)


def test_calling_when_no_params():
    function = fun.curryable(lambda a: 1)
    got = function(1)
    assert got == 1


def test_calling_curried_function():
    function = fun.curryable(lambda a, b: 1)
    got = function(1)(2)
    assert got == 1


def test_compose():
    def f(a):
        return a + 1  # pragma: no cover

    def g(a):
        return a * 2  # pragma: no cover
    assert fun.compose(f, g)(1) == 3


def test_compose_repr():
    got = repr(fun.compose(lambda x: 1, lambda: 1))  # pragma: no branch
    assert got.startswith('compose(')


def test_is_fully_bound_no_params():
    assert fun._is_fully_bound(lambda: 1, ())  # pragma: no branch


def test_is_fully_bound_missing_arg():
    assert not fun._is_fully_bound(lambda x: 1, ())  # pragma: no branch


def test_is_fully_bound_with_param():
    assert fun._is_fully_bound(lambda x: 1, (1,))  # pragma: no branch
