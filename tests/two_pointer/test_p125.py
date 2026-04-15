import pytest

from solutions.two_pointer.p125 import is_palindrome


@pytest.mark.parametrize(
    "text, output",
    [("A man, a plan, a canal: Panama", True), ("race a car", False), (" ", True)],
)
def test_p125(text, output):
    assert is_palindrome(text) == output
