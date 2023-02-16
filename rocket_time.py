import time


def time_diff (final_time, init_time):
    return (final_time - init_time)

def get_time ():
    return time.monotonic_ns() / 1_000_000