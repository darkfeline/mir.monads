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

"""Tests for _is_fully_bound."""

import pytest

from mir.monads.abc import _is_fully_bound


@pytest.mark.parametrize(
    'f,args,expected', [
        (lambda: 1, (), True),
        (lambda a: 1, (), False),
        (lambda a: 1, (1,), True),
        (lambda a, b: 1, (1,), False),
    ])
def test__is_fully_bound(f, args, expected):
    got = _is_fully_bound(f, args)
    assert bool(got) == expected
