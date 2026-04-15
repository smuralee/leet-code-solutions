import pytest

from solutions.two_pointer.p11 import container_with_water


@pytest.mark.parametrize(
    "height,area", [([1, 8, 6, 2, 5, 4, 8, 3, 7], 49), ([1, 1], 1)]
)
def test_p11(height, area):
    assert container_with_water(height) == area
