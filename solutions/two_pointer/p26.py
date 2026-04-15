def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    write = 1  # Write points to the element which has to be swapped next
    # Scan through the array, moving unique elements to the front, start from index=1
    for read in range(1, len(nums)):
        # Check if the adjacent elements match
        if nums[read] != nums[read - 1]:
            # If not, it's time to change the write pointer position
            nums[write] = nums[read]
            # Increment the swap position
            write += 1
    return write
