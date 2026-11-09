# Digit Counter (Q3: Count the digits)
Zeyad Hosny: Class Participation Activity W12 (Recursion in Python), BGSU, Fall 2026.

A small Python program that reads a non-negative integer and prints how many digits it has. The counting is done by a recursive function, digit_count(), and every input is validated by main.py: an invalid entry is reported with its reason and asked again, instead of crashing the program.



## 1. Repository contents

- recursion.py: the recursive digit_count() function. It takes a non-negative integer and returns its number of digits. It contains no input handling.
- main.py: the program. It prompts for a number, validates it, calls digit_count(), prints the result, and asks whether to continue. This is the file you run.
- efficiency_metrics.py: measures the mean runtime and stack depth of digit_count() against an equivalent loop on small numbers (1 to 100000). It produces the efficiency results in the presentation; see section 11.
- README.md: this file.

- Note: main.py and efficiency_metrics.py both import recursion.py, so please keep all three files in the same folder.


## 2. Environment setup

- Python 3 (developed and tested on Python 3.12.10).
- Standard library only: no third-party packages and nothing to install. main.py imports only sys (built in) and recursion, from the same folder; efficiency_metrics.py also uses statistics and timeit, both part of the standard library. There is no requirements.txt because there is nothing to install.
- Tested in Git Bash on Windows. Nothing in the code is platform-specific, so it should run in any terminal that has Python 3.

- Note: to check your Python version:
```
python --version
```


## 3. Dataset

This project uses no dataset. The program is interactive: all data is typed in at the prompts. The reference case is the worked example from the activity (345 has 3 digits), reproduced as Example 1 in section 10. The inputs of the efficiency measurements (1, 10, 100, 1000, 10000 and 100000) are fixed in efficiency_metrics.py (section 11).


## 4. How to run

Open a terminal in the folder that contains recursion.py and main.py, then run:

```
python main.py
```

Note: (On macOS/Linux you may need "python3 main.py")

The program asks for a number, prints its digit count, then asks whether you want to count the digits of another number. Answer 'n' to finish.

To stop at any time, press Ctrl+C. Signalling end of input (Ctrl+D in macOS/Linux terminals, Ctrl+Z then Enter in a Windows console) does the same. In both cases the program prints "Input ended unexpectedly. Exiting." and exits cleanly instead of showing an error trace.

To reproduce the efficiency results, run "python efficiency_metrics.py" (see section 11).


## 5. Inputs

The program prompts for these values, in this order:

1. Number (integer): a non-negative whole number, up to 800 characters long (see the note below). Default if left blank: 0.
2. Count another number? (string): y, Y, n or N. No default: a blank answer is asked again.

Note:
- Leading and trailing spaces are ignored.
- Leaving the number blank (by pressing Enter) is a deliberate "skip": the default 0 is used and no error is shown.
- Leading zeros are dropped before counting, because the input is converted to an int first: 007 is counted as 7 (1 digit).
- An optional leading sign is accepted: +12 is read as 12 and -0 as 0.
- The 800 limit counts the characters typed (after the surrounding spaces are removed), so a sign or leading zeros count toward it.


## 6. How the recursion works

digit_count() uses the hint from the activity: integer division by 10 (num // 10) removes the last digit, and the count goes up by 1 each time.

- Base case: a number below 10 (0 to 9) has one digit, so the function returns 1.
- Recursive case: otherwise it returns 1 + digit_count(num // 10).

Trace for 345:

```
digit_count(345)
= 1 + digit_count(34)
= 1 + 1 + digit_count(3)
= 1 + 1 + 1          <- base case: 3 < 10 returns 1
= 3
```

- 0 returns 1, since "0" is written with one digit.
- A d-digit number takes d calls in total, one per digit (the first call plus d - 1 recursive calls), so the input length is limited by Python's recursion limit (see section 8).


## 7. How to read the output

Using Example 1 (below), the result line reads like this:

```
The number 345 has the following number of digits: 3
           ^^^                                     ^
           the number that was counted             the value returned by digit_count()
```

When the user answers 'n', the program prints "User chose to stop. Exiting." and ends.

Note: the activity's example shows the output as just 3. The program prints the same value, returned by digit_count(), inside a full sentence so that it is clear which number was counted.


## 8. Error handling

Every prompt is validated. The rules are:

- Number: rejected when the text contains letters or _, is a decimal, contains a comma, is longer than 800 characters, is a malformed number, or is negative. Examples: abc, nan, 1e5, 1_000, 3.5, 1,000, -5, 1-2
- Count another number?: rejected when it is anything other than y, Y, n or N (including blank). Example: maybe

What happens on a rejected entry:

1. The program prints a message naming the reason, for example: Invalid number: '3.5' is a decimal, not an integer. Please try again.
2. It asks again, up to 10 attempts in total.
3. If the last attempt is also invalid, it prints the reason, uses the default value 0 and continues.
4. The Y/N question is different: it has no sensible default, so it keeps asking until it gets a valid answer.

Limitation: entries such as 1e5 (scientific notation for 100000), 1_000 (Python's digit separator, which int() accepts as 1000) and 1,000 are valid ways to write a whole number, but the program does not support these formats and rejects them. Malformed text such as 1-2 passes the earlier checks and is rejected by int(); its error is replaced with the same "is not a valid number" message instead of Python's own.


## 9. Parameters

There are no command-line options or configuration files. The limits and defaults are constants at the top of main.py and efficiency_metrics.py; edit them there if you want different values.

In main.py:

- DEFAULT_NUMBER_VALUE = 0: default number (used when the value is blank, or still invalid after the last attempt).
- RECURSION_SAFETY_MARGIN = 200: stack frames kept free for the code that calls digit_count().
- MAX_NUMBER_LENGTH = sys.getrecursionlimit() - RECURSION_SAFETY_MARGIN: longest accepted input, in characters. With Python's default recursion limit of 1000 this is 800. It is calculated once, when main.py is loaded, from the recursion limit at that moment; a later sys.setrecursionlimit() call does not update it.
- MAX_NUM_ATTEMPTS = 10: maximum attempts per input (first entry + retries). Must be an integer greater than 0.

In efficiency_metrics.py:

- SAMPLE_INPUTS = (1, 10, 100, 1000, 10000, 100000): the numbers measured (1 to 6 digits). They are small, so each // 10 takes constant time.
- NUM_RUNS = 7: timed runs per input; the reported time is their mean.
- CALLS_PER_RUN = 10000: calls in one timed run. One call is too short for the timer, so the run's total time is divided by this number.

In recursion.py, the constants define the algorithm itself and are named only to avoid magic numbers; they are not settings to change:

- NUMBER_BASE = 10: dividing by it removes the last digit.
- SINGLE_DIGIT_LIMIT = NUMBER_BASE: numbers below it are the base case (one digit).
- ONE_DIGIT = 1: the count added at each recursive step and returned by the base case.


## 10. Working examples

- Four examples, each run with the real program. Text after a prompt's colon is what was typed.
- When Enter is pressed on a blank line, you will see nothing follows the colon.
- Example 1 is the example given in the activity.

- Example 1, 345: Result: 3. Shows: activity example.
- Example 2, 0, blank and 7: Result: 1 each. Shows: base case, default value.
- Example 3, 12, 2026 and 1000000: Result: 2, 4, 7. Shows: several numbers in one run, Y and y both accepted.
- Example 4, invalid entries: abc, 3.5, 1,000, -5, 1e5 and 1-2 are rejected, then 2026 is accepted. Shows: error handling, retry.

### Example 1: 345 (activity example)

```
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 345
The number 345 has the following number of digits: 3

Do you want to count the digits of another number? 'y/Y' or 'n/N': n

User chose to stop. Exiting.
```

### Example 2: Single digits and the default value

0 is a single digit, so it returns 1 straight from the base case. The second entry is blank, so the default 0 is used.

```
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 0
The number 0 has the following number of digits: 1

Do you want to count the digits of another number? 'y/Y' or 'n/N': y
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 
The number 0 has the following number of digits: 1

Do you want to count the digits of another number? 'y/Y' or 'n/N': y
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 7
The number 7 has the following number of digits: 1

Do you want to count the digits of another number? 'y/Y' or 'n/N': n

User chose to stop. Exiting.
```

### Example 3: Several numbers in one run

```
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 12
The number 12 has the following number of digits: 2

Do you want to count the digits of another number? 'y/Y' or 'n/N': y
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 2026
The number 2026 has the following number of digits: 4

Do you want to count the digits of another number? 'y/Y' or 'n/N': Y
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 1000000
The number 1000000 has the following number of digits: 7

Do you want to count the digits of another number? 'y/Y' or 'n/N': n

User chose to stop. Exiting.
```

### Example 4: Error handling

- abc and 1e5 are rejected (contain letters).
- 3.5 is rejected (decimal), 1,000 is rejected (comma) and -5 is rejected (negative).
- 1-2 passes the earlier checks but is rejected by int() (malformed number).
- 2026 is accepted: 4 digits.
- At the final question, maybe is not a valid answer, so it is asked again.

```
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): abc
Invalid number: 'abc' is not a valid number. Please try again.
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 3.5
Invalid number: '3.5' is a decimal, not an integer. Please try again.
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 1,000
Invalid number: '1,000' contains a comma; enter digits only (e.g. 1000). Please try again.
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): -5
Invalid number: -5 is negative. Please try again.
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 1e5
Invalid number: '1e5' is not a valid number. Please try again.
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 1-2
Invalid number: '1-2' is not a valid number. Please try again.
Enter a non-negative integer (up to 800 digits, or leave blank to use the default of 0): 2026
The number 2026 has the following number of digits: 4

Do you want to count the digits of another number? 'y/Y' or 'n/N': maybe
Invalid response: 'maybe' is not 'Y' or 'N'. Please try again.

Do you want to count the digits of another number? 'y/Y' or 'n/N': n

User chose to stop. Exiting.
```


## 11. Efficiency measurements

efficiency_metrics.py produces the efficiency results in the presentation. It compares digit_count() with an equivalent loop, digit_count_loop() (defined in the same file), on six small numbers. Run it from the same folder; it needs no input and finishes in under a second:

```
python efficiency_metrics.py
```

Output of the run used in the presentation (Python 3.12.10). The times will be slightly different on every run (see "What to expect" below); the frame counts will not:

```
Runtime = mean of 7 runs x 10000 calls, in microseconds (us)

  Input  Digits  Rec. time  Loop time  Rec. time/digit  Rec. frames  Loop frames
      1       1      0.040      0.040            0.040            1            1
     10       2      0.084      0.074            0.042            2            1
    100       3      0.126      0.105            0.042            3            1
   1000       4      0.172      0.131            0.043            4            1
  10000       5      0.219      0.175            0.044            5            1
 100000       6      0.269      0.219            0.045            6            1
```

How to read the columns:

- Input: the number measured. Digits: its number of digits, d.
- Rec. time / Loop time: mean time of one call of the recursive and the loop version, in microseconds. Each is the mean of NUM_RUNS (7) runs, and each run times CALLS_PER_RUN (10000) calls.
- Rec. time/digit: the recursive time divided by d. It stays about the same as d grows, so the runtime grows linearly with the number of digits: O(d).
- Rec. frames / Loop frames: stack frames used. The script counts the calls of each function; for digit_count(), every call is still on the stack when the last one runs, so the count equals the stack depth. The recursion uses d frames, O(d) memory; the loop always uses 1, O(1). This counts frames, not bytes.

What to expect when you run it:

- The frame counts are always the same.
- The times change slightly between runs and between computers, so they will not match the table exactly. They depend on many factors, such as the processor and its current speed (power-saving or turbo modes), other programs running at the same time, the operating system and the Python version. Taking the mean of 7 runs reduces this variation but cannot remove it.
- The trend should still hold: the time per digit stays roughly constant, and the loop is faster once the number has more than one digit (~19% less time for 100000 in the run above).

