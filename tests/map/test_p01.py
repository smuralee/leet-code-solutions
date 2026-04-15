import pytest
from solutions.map.p01 import two_sum_unsorted


@pytest.mark.parametrize(
    "nums, target, expected",
    [
        # basic cases
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        # duplicates
        ([3, 3], 6, [0, 1]),
        # negatives
        ([-1, -2, -3, -4], -6, [1, 3]),
        # zero
        ([0, 4, 3, 0], 0, [0, 3]),
        # no match
        ([1, 2, 3], 10, []),
        # two elements
        ([1, 4], 5, [0, 1]),
    ],
)
def test_p01(nums, target, expected):
    assert two_sum_unsorted(nums, target) == expected
