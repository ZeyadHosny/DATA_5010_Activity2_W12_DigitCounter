# Base of the decimal number system; dividing by it removes the last digit.
NUMBER_BASE = 10
# Every non-negative integer below NUMBER_BASE (0-9) has exactly one digit.
SINGLE_DIGIT_LIMIT = NUMBER_BASE
# Digit count added for each digit removed (and for the base case).
ONE_DIGIT = 1

# Function to count the digits of a non-negative integer recursively
def digit_count(num):
    """
    Description:
    - Return the number of digits in a non-negative integer, using recursion.
    - Base case: a single-digit number (0-9) has one digit, so 0 returns 1.
    - Recursive case: integer division by 10 removes the last digit, and the
    count increases by 1 for each removed digit.

    Input arguments:
        num (int): The non-negative integer whose digits are counted.

    Return:
        int: The number of digits in `num`.
    """
    # Base case: only one digit is left.
    if num < SINGLE_DIGIT_LIMIT:
        return ONE_DIGIT
    # Recursive case: count the last digit and recurse on the remaining digits.
    return ONE_DIGIT + digit_count(num // NUMBER_BASE)
