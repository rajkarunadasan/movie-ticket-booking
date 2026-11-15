import pytest

from app import validators as v


@pytest.mark.parametrize("value,ok", [("Asha Devi", True), ("", False), ("1234", False)])
def test_name(value, ok):
    assert (v.validate_name(value)[1] is None) == ok


@pytest.mark.parametrize("value,expected", [
    ("Asha@Mail.com", "asha@mail.com"), ("bad", None), ("a@b", None), ("", None)])
def test_email(value, expected):
    assert v.validate_email(value)[0] == expected


@pytest.mark.parametrize("value,ok", [
    ("abcdef12", True), ("short1", False), ("allletters", False), ("12345678", False)])
def test_password(value, ok):
    assert (v.validate_password(value)[1] is None) == ok


def test_seats():
    assert v.validate_seats(["a2", "A1", "A1"])[0] == ["A1", "A2"]
    assert v.validate_seats([])[1]
    assert v.validate_seats(["Z9"])[1]
    assert v.validate_seats([f"A{i}" for i in range(1, 8)])[1]


def test_payment_and_review():
    assert v.validate_payment("UPI")[1] is None
    assert v.validate_payment("Cash")[1]
    assert v.validate_review("5", "Great")[2] is None
    assert v.validate_review("9", "Great")[2]
    assert v.validate_review("3", "")[2]
