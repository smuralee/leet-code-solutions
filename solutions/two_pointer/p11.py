def container_with_water(height: list[int]) -> int:
    """
    Time complexity: O(n)
    Space complexity: O(1)
    """
    left, right = (0, len(height) - 1)
    area = 0
    while left < right:
        w = right - left
        h = min(height[left], height[right])
        area = max(area, w * h)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return area
