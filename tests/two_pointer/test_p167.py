import pytest

from solutions.two_pointer.p167 import two_sum_sorted


@pytest.mark.parametrize(
    "nums, target, expected",
    [([2, 7, 11, 15], 9, [1, 2]), ([2, 3, 4], 6, [1, 3]), ([-1, 0], -1, [1, 2])],
)
def test_p167(nums, target, expected):
    assert two_sum_sorted(nums, target) == expected
