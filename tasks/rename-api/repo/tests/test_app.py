import pytest

from app.admin import is_admin
from app.api import user_profile
from app.notifications import welcome_email
from app.users import get_user


def test_get_user():
    assert get_user(1)["name"] == "Alice"


def test_unknown_user():
    with pytest.raises(KeyError):
        get_user(99)


def test_profile():
    assert user_profile(2) == {"id": 2, "name": "Bob"}


def test_admin():
    assert is_admin(1) and not is_admin(2)


def test_welcome_email():
    assert welcome_email(2) == "To: bob@example.com\nHello Bob!"
