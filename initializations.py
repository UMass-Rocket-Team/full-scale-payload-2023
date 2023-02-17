import time
import rocket_queue

#init_time = time.monotonic_ns() / 1_000_000
init_time = time.ticks_ms()
time_queue = None
accel_queue = None
altitude_queue = None
