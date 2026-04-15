def is_palindrome(text: str) -> bool:
    left, right = (0, len(text) - 1)
    # Keep going until pointers meet
    while left < right:
        # skip invalid characters on the left
        while left < right and not text[left].isalnum():
            left += 1
        # skip invalid characters on the right
        while left < right and not text[right].isalnum():
            right -= 1
        # compare the values
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True
