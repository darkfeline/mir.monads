from mir.monads import base
from mir.monads.base import unit


def test_then():
    assert unit(1, base.Identity).then(2) == 2


def test_eq():
    assert unit(1, base.Identity) != 1
