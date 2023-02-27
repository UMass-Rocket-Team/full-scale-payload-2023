# calculate maximum size of queue needed by frequency (samples/s) * interval to keep track of (ms) / 1000 (ms/s) * 1.25 room for error
import rocket_time
from math import floor, hypot
from rocket_queue import Queue
import rocket_intializations
from singleton import Singleton
def calculate_max_size(sample_frequency, queue_interval):
    return floor(sample_frequency * queue_interval / 1000 * 1.25)


class RocketController(metaclass=Singleton):
    def __init__(self):
        self.time_queue = None
        self.accel_queue = None
        self.altitude_queue = None
        self.imu = rocket_intializations.RocketIMU()
        self.pressure_sensor = rocket_intializations.RocketPressureSensor()
        self.timer = rocket_time.RocketTimer()
    # Inputs: Array of functions that should be run every x ms
    # 		Array of intervals of time between each run of its corresponding function
    # Outputs: None
    # Each function in func_arr should raise an exception if the loop should stop being run
    def do_every(self, func_arr, interval_arr):
        prev_times = [-999999] * len(func_arr)
        while True:
            for i, func in enumerate(func_arr):
                #if time.ticks_diff(time.ticks_ms(), prev_times[i]) > interval_arr[i]:
                if rocket_time.RocketTimer.time_since_ms(prev_times[i]) > interval_arr[i]:
                    try:
                        func()
                        prev_times[i] = rocket_time.RocketTimer.get_time_ms()
                    except StopIteration:  # Leave the while loop
                        return

    # Inputs: Interval: How much acceleration data should be kept track of (eg last 2000 ms, interval = 2000)
    # 						NOTE: This does not mean acceleration is updated every interval ms
    # Output: A function that can be passed into do_every to update the time and acceleration queues
    def make_data_updater(self, queue_frequency, time_interval, threshold_tuple):
        max_size = calculate_max_size(queue_frequency, time_interval)
        self.time_queue = Queue(max_size, threshold_tuple[0])
        self.accel_queue = Queue(max_size, threshold_tuple[1])
        self.altitude_queue = Queue(max_size, threshold_tuple[2])
        def updater():
            cur_time = self.timer.time_since_init_ms()
            self.time_queue.enqueue(cur_time)
            self.accel_queue.enqueue(hypot(*(self.imu.accel())))
            self.altitude_queue.enqueue(self.pressure_sensor.altitude())
            #while time.ticks_diff(cur_time, self.time_queue.peek()) > time_interval:
            while rocket_time.RocketTimer.time_since_ms(self.time_queue.peek()) > time_interval:
                self.time_queue.dequeue()
                self.accel_queue.dequeue()
                self.altitude_queue.dequeue()
        return updater