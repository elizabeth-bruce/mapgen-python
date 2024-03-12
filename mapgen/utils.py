import cProfile
import random
import sys
import string

from contextlib import contextmanager


@contextmanager
def cpu_profiler():
    pr = cProfile.Profile()
    pr.enable()
    try:
        yield pr
    finally:
        pr.disable()
        lid = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        pr.dump_stats(f"profiles/cpu_{lid}.prof")
        with open(f"profiles/cpu_{lid}.txt", "w") as output_file:
            sys.stdout = output_file
            pr.print_stats(sort="time")
            sys.stdout = sys.__stdout__
