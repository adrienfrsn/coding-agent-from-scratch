import pytest

from stack import Stack


def test_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1


def test_peek():
    s = Stack()
    s.push(7)
    assert s.peek() == 7
    assert len(s) == 1


def test_pop_empty():
    with pytest.raises(IndexError):
        Stack().pop()


def test_is_empty():
    s = Stack()
    assert s.is_empty()
    s.push(1)
    assert not s.is_empty()
