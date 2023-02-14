import time
import queue

init_time = time.monotonic_ns() / 1_000_000
time_queue = None
accel_queue = None
altitude_queue = None
