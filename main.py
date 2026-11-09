import sys

from recursion import digit_count

# Zero value to avoid magic numbers.
ZERO_VALUE = 0
# Default number used when the input is blank or invalid.
DEFAULT_NUMBER_VALUE = 0
# --- Input limits ------------------------------------------------
# Recursion safety margin for digit_count() calls.
RECURSION_SAFETY_MARGIN = 200
# Maximum digits accepted: one recursive call per digit, so bounded by the recursion limit (default 1000) - Margin (RECURSION_SAFETY_MARGIN).
MAX_NUMBER_LENGTH = sys.getrecursionlimit() - RECURSION_SAFETY_MARGIN
# Maximum number of attempts allowed per input (initial entry + retries). Must be an integer greater than 0.
MAX_NUM_ATTEMPTS = 10
# Index of the last attempt (attempt indices run 0 .. MAX_NUM_ATTEMPTS - 1).
LAST_ATTEMPT = MAX_NUM_ATTEMPTS - 1


def looks_numeric(text):
    """
    Description:
    - Check if a string does not contain letters and underscores.
    - Examples of rejected formats are ("abc", "nan", "inf", "1e10", "1_000").
    - The malformed text (e.g. "1-2", "--5") passes this check
    and is rejected afterwards when int() fails to convert it.

    Input arguments:
        text (str): The string to check.

    Return:
        bool: True if `text` does not contain letters and underscores, False otherwise.
    """
    for character in text:
        # A letter or underscore means the text is not plain numeric input.
        if character.isalpha() or character == "_":
            return False
    return True


def read_number():
    """
    Description:
    - Prompt for a non-negative integer and return it as an int.
    - A blank entry returns the default 0. An invalid entry is re-prompted
    until the last allowed attempt, then 0 is used.

    Input arguments:
        None

    Return:
        int: The non-negative integer entered by the user.
    """
    prompt = (f"Enter a non-negative integer (up to {MAX_NUMBER_LENGTH} digits, "
              f"or leave blank to use the default of {DEFAULT_NUMBER_VALUE}): ")

    # Retries until the last allowed attempt (MAX_NUM_ATTEMPTS total), then falls back to the default.
    for attempt in range(MAX_NUM_ATTEMPTS):
        # Request the user to input the number and deletes trailing/leading whitespace.
        raw_value = input(prompt).strip()

        # Blank input is a deliberate skip, not an error. It is checked before
        # validation so it is never reported as an invalid number.
        if raw_value == "":
            return DEFAULT_NUMBER_VALUE

        # Each check below raises ValueError with a message naming its problem.
        try:
            # Error handled: text contains a letter or an underscore ("abc", "1_000", "1e100").
            if not looks_numeric(raw_value):
                raise ValueError(f"'{raw_value}' is not a valid number")
            # Error handled: decimal value ("3.5", "10.0"); only whole numbers have a digit count.
            if "." in raw_value:
                raise ValueError(f"'{raw_value}' is a decimal, not an integer")
            # Error handled: thousands separator ("1,000"); enter digits only.
            if "," in raw_value:
                raise ValueError(f"'{raw_value}' contains a comma; enter digits only (e.g. 1000)")
            # Error handled: number is longer than MAX_NUMBER_LENGTH characters.
            if len(raw_value) > MAX_NUMBER_LENGTH:
                raise ValueError(f"exceeds the {MAX_NUMBER_LENGTH}-digit limit")
            # Error handled: malformed text that passed the checks above ("1-2", "--5", "1 0", "-");
            # int() raises ValueError itself, replaced here with a clearer message.
            try:
                value = int(raw_value)
            except ValueError:
                raise ValueError(f"'{raw_value}' is not a valid number") from None
            # Error handled: negative number.
            if value < ZERO_VALUE:
                raise ValueError(f"{value} is negative")
        # Error handled: any invalid-number ValueError raised above.
        except ValueError as error:
            # Last allowed attempt: report the reason and use the default.
            if attempt == LAST_ATTEMPT:
                print(f"Invalid number: {error}. Using default value {DEFAULT_NUMBER_VALUE}.")
                return DEFAULT_NUMBER_VALUE
            # Not the last allowed attempt yet: report the reason and ask again.
            print(f"Invalid number: {error}. Please try again.")
            continue
        # Error handled: any unexpected exception other than ValueError
        # (safety procedure), treated like an invalid entry.
        # Exception (not a bare except) lets Ctrl+C and exit requests reach main().
        except Exception:
            if attempt == LAST_ATTEMPT:
                print(f"Something unexpected happened while reading the number. "
                      f"Using default value {DEFAULT_NUMBER_VALUE}.")
                return DEFAULT_NUMBER_VALUE
            print("Something unexpected happened while reading the number. "
                  "Please try again.")
            continue

        return int(value)


def read_continue_choice():
    """
    Description:
    - Ask whether to count the digits of another number and return "y/Y" or "n/N".
    - Re-prompts until the answer is valid.
    - If "Ctrl+C" or "end of input" is entered, it will be handled in the main loop.

    Input arguments:
        None

    Return:
        str: "y" or "n" based on the user's choice.
    """
    prompt = "\nDo you want to count the digits of another number? 'y/Y' or 'n/N': "

    while True:
        # Request the user to input their choice and deletes trailing/leading whitespace and lowercases it.
        choice = input(prompt).strip().lower()
        if choice in ("y", "n"):
            return choice
        # Error handled: any answer other than Y/y/N/n (including blank);
        # report it and ask again.
        print(f"Invalid response: '{choice}' is not 'Y' or 'N'. Please try again.")


def main():
    """
    Description:
    - Run the program: each pass reads one number, prints its digit count, then asks
    whether to continue, so the loop always runs at least once.
    - Any input() call can raise EOFError or KeyboardInterrupt, so they are
    handled once here instead of inside every read function.
    """
    try:
        while True:
            # Request the user to input a non-negative integer.
            number = read_number()
            # Count the digits of the number using the recursive function.
            num_digits = digit_count(number)
            # Print the digit count for the current number.
            print(f"The number {number} has the following number of digits: {num_digits}")
            # Ask the user whether to continue or not.
            if read_continue_choice() == "n":
                print("\nUser chose to stop. Exiting.")
                break
    # Error handled: the input stream ended (EOFError, e.g. Ctrl+D "Unix-like terminals" or ctrl +z +enter "windows") or the user
    # pressed Ctrl+C (KeyboardInterrupt); exit cleanly instead of a traceback.
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended unexpectedly. Exiting.")


# Run main() only when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    main()
