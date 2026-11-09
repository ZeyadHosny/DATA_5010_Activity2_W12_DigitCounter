import statistics
import sys
import timeit

from recursion import digit_count

# Small numbers (1 to 6 digits), so each // 10 takes constant time (standard model).
SAMPLE_INPUTS = (1, 10, 100, 1000, 10000, 100000)
# Each runtime is the mean of NUM_RUNS runs; one run times CALLS_PER_RUN calls.
NUM_RUNS = 7
CALLS_PER_RUN = 10000
MICROSECONDS_PER_SECOND = 1000000


def digit_count_loop(num):
    """
    Description:
    - Loop version of digit_count(), used only for comparison.

    Input arguments:
        num (int): The non-negative integer whose digits are counted.

    Return:
        int: The number of digits in `num`.
    """
    count = 1
    while num >= 10:
        num //= 10
        count += 1
    return count


def mean_runtime(function, num):
    """
    Description:
    - Return the mean time of one call of function(num).
    - One call is shorter than the timer's resolution, so each run times
    CALLS_PER_RUN calls and divides the total by CALLS_PER_RUN.
    - The run is repeated NUM_RUNS times and the mean is reported to smooth out noise.

    Input arguments:
        function (callable): The function to time.
        num (int): The number passed to the function.

    Return:
        float: Mean time of one call, in microseconds.
    """
    run_times = timeit.repeat("function(num)", globals={"function": function, "num": num},
                              repeat=NUM_RUNS, number=CALLS_PER_RUN)
    return (statistics.mean(run_times) / CALLS_PER_RUN) * MICROSECONDS_PER_SECOND


def stack_depth(function, num):
    """
    Description:
    - Count the calls of `function` while it computes function(num).
    - Every call stays on the stack until the last one returns, so the
    number of calls is the stack depth (frames).

    Input arguments:
        function (callable): The function to measure.
        num (int): The number passed to the function.

    Return:
        int: The number of stack frames used.
    """
    # Number of calls of `function` counted so far.
    calls = 0

    # Profiler callback; Python passes (frame, event, arg) on every call and return.
    def count_call(frame, event, arg):
        # Update the counter defined in stack_depth().
        nonlocal calls
        # Count only new frames that run `function`; frames of other code are skipped.
        if event == "call" and frame.f_code is function.__code__:
            # One more frame of `function` is on the stack.
            calls += 1

    # Start profiling: count_call() now runs on every call and return.
    sys.setprofile(count_call)
    # Run the function once while its calls are counted.
    function(num)
    # Stop profiling so no later calls are counted.
    sys.setprofile(None)
    # Calls equal the stack depth, since every call stays on the stack until the last one returns.
    return calls


def main():
    """
    Description:
    - Print the mean runtime and stack depth of the recursive and loop versions
    for each number in SAMPLE_INPUTS.
    """
    print(f"Runtime = mean of {NUM_RUNS} runs x {CALLS_PER_RUN} calls, in microseconds (us)\n")
    print(f"{'Input':>7} {'Digits':>7} {'Rec. time':>10} {'Loop time':>10} {'Rec. time/digit':>16} "
          f"{'Rec. frames':>12} {'Loop frames':>12}")

    for num in SAMPLE_INPUTS:
        digits = digit_count(num)
        rec_time = mean_runtime(digit_count, num)
        loop_time = mean_runtime(digit_count_loop, num)
        print(f"{num:>7} {digits:>7} {rec_time:>10.3f} {loop_time:>10.3f} {rec_time / digits:>16.3f} "
              f"{stack_depth(digit_count, num):>12} {stack_depth(digit_count_loop, num):>12}")


# Run main() only when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    main()
