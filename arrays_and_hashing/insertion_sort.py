from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Insertion sort algorithm

    Args:
        arr:List[int] to be sorted

    Returns:
        Sorted list
    """

    # Get the length of the array
    n = len(arr)

    # If the array has only one element, return same array
    if n <= 1:
        return arr

    # Loop from the 1st index of the array
    # We need two markers, current(i) and previous(j)
    # Previous will run from current - 1, all the way to the 0th index position
    # Hence we keep decrementing j index and use a while loop
    for i in range(1, n):
        key = arr[i]
        j = i - 1

        # Keep swapping, till the key is less than previous
        while j >= 0 and key < arr[j]:
            # Moving the element, one position to the right, then reducing the j index
            arr[j + 1] = arr[j]
            j -= 1

        # Once all the values greater than key are moved to the right by one position
        # Set the key in the empty slot
        arr[j + 1] = key

    return arr


print(insertion_sort([7, 5, 2, 1, 6]))
