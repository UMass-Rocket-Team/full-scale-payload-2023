# calculate maximum size of queue needed by frequency (samples/s) * interval to keep track of (ms) / 1000 (ms/s) * 1.25 room for error
from math import floor, hypot
import time
from queue import Queue
from imu_setup import imu
from pressure_sensor_setup import pressure_sensor

def calculate_max_size(sample_frequency, queue_interval):
    return floor(sample_frequency * queue_interval / 1000 * 1.25)

# Inputs: Array of functions that should be run every x ms
# 		Array of intervals of time between each run of its corresponding function
# Outputs: None
# Each function in func_arr should raise an exception if the loop should stop being run
def do_every(func_arr, interval_arr):
    prev_times = [-999999] * len(func_arr)
    while True:
        for i, func in enumerate(func_arr):
            if time.ticks_diff(time.ticks_ms(), prev_times[i]) > interval_arr[i]:
                try:
                    func()
                    prev_times[i] = time.ticks_ms()
                except StopIteration:  # Leave the while loop
                    return

# Inputs: Interval: How much acceleration data should be kept track of (eg last 2000 ms, interval = 2000)
# 						NOTE: This does not mean acceleration is updated every interval ms
# Output: A function that can be passed into do_every to update the time and acceleration queues
def make_data_updater(queue_frequency, time_interval, threshold_tuple, queue_tuple):
    max_size = calculate_max_size(queue_frequency, time_interval)

    queue_tuple[0] = Queue(max_size, None)
    queue_tuple[1] = Queue(max_size, threshold_tuple[0])
    queue_tuple[2] = Queue(max_size, threshold_tuple[1])

    def updater():
        cur_time = time.ticks_ms()
        time_queue.enqueue(cur_time)
        accel_data = imu.accel()
        accel_queue.enqueue(hypot(*accel_data))
        altitude_queue.enqueue(pressure_sensor.altitude())
        while time.ticks_diff(cur_time, time_queue.peek()) > time_interval:
            time_queue.dequeue()
            accel_queue.dequeue()
            altitude_queue.dequeue()
    return updater