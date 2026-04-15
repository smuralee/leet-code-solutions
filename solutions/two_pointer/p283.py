def move_zeroes(nums: list[int]) -> None:
    # 'write' tracks the index where the next non-zero number belongs
    write = 0
    # Move the read pointer across the list
    for read in range(len(nums)):
        # When we find a non-zero, swap it forward to the 'write' position
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            # Move 'write' to the next available slot
            write += 1
