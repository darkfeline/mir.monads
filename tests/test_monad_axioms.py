import pytest

from mir import protology

from mir.monads import monads
from mir.monads.monads import compose
from mir.monads.monads import unit


@pytest.mark.parametrize('g,a,mtype', [
    (lambda a, mtype: unit(a + 1, mtype), 1, monads.Identity),
])
def test_left_identity(g, a, mtype):
    """return >=> g ≡ g"""
    assert compose(unit, g)(a, mtype) == g(a, mtype)


@pytest.mark.parametrize('f,a,mtype', [
    (lambda a, mtype: unit(a + 1, mtype), 1, monads.Identity),
])
def test_right_identity(f, a, mtype):
    """f >=> return ≡ f"""
    assert compose(f, unit)(a, mtype) == f(a, mtype)


@pytest.mark.parametrize('f,g,h,a,mtype', [
    (lambda a, mtype: unit(a + 1, mtype),
     lambda a, mtype: unit(a * 2, mtype),
     lambda a, mtype: unit(a ** 3, mtype),
     1, monads.Identity),
])
def test_associativity(f, g, h, a, mtype):
    """(f >=> g) >=> h ≡ f >=> (g >=> h)"""
    assert compose(compose(f, g), h)(a, mtype) \
        == compose(f, compose(g, h))(a, mtype)


@pytest.mark.parametrize('f,a,mtype', [
    (lambda a, mtype: unit(a + 1, mtype), 1, monads.Identity),
])
def test_bind_left_identity(f, a, mtype):
    """return a >>= f ≡ f a"""
    assert unit(a, mtype).bind(f) == f(a, mtype)


@pytest.mark.parametrize('m', [
    unit(1, monads.Identity),
])
def test_bind_right_identity(m):
    """m >>= return ≡ m"""
    assert m.bind(unit) == m


@pytest.mark.parametrize('m,f,g', [
    (unit(1, monads.Identity),
     lambda a, mtype: unit(a + 1, mtype),
     lambda a, mtype: unit(a * 2, mtype)),
])
def test_bind_associativity(m, f, g):
    r"""(m >>= f) >>= g ≡ m >>= (\x -> f x >>= g)"""
    assert m.bind(f).bind(g) == m.bind(lambda x, mtype: f(x, mtype).bind(g))
