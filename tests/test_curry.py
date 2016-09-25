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

"""Tests for curry decorator."""

from mir.monads.abc import curry


def test_currying_when_unbound_params():
    function = curry(lambda a, b: 1)
    got = function(1)
    assert callable(got)


def test_calling_when_no_params():
    function = curry(lambda a: 1)
    got = function(1)
    assert got == 1


def test_calling_curried_function():
    function = curry(lambda a, b: 1)
    got = function(1)(2)
    assert got == 1
