import machine
import uos
from imu_setup import imu, write_to_imu_data, calibration_fn
from pressure_sensor_setup import pressure_sensor, get_altitude
from rocket_queue import Queue
from math import floor
import time


# from sys import exit  # only for testing

"""
SUBSCALE PAYLOAD CONTROL Version 1.0-alpha
Authors: Payload Sub-Team
Since: 11/09/2022
Created for University of Massachusetts Rocket Team (Payload Sub-Team)
This program collects and stores data from the BNO055 IMU, detects launch and landing, and orients to ground upon landing.
"""



# IF YOU ARE IMPLEMENTING DATA TRANSMISSIONS, READ THE BELOW TEXT:
# To add transmissions, use uart.write(string)


class ForceLandingException(Exception):
    pass


init_time = time.ticks_ms()


def mean(arr, length):
    sum = 0
    for e in arr:
        if e != None:
            sum += e
    return sum / length


# Input: Queue to find mean/variance
# Output: array: [mean, variance]
def mean_variance(queue):
    size = queue.get_size()
    arr = queue.get_array()
    mean_val = mean(arr, size)
    sum = 0
    for e in arr:
        if e != None:
            sum += (e - mean_val) ** 2
    return [mean_val, sum / size]


# calculate maximum size of queue needed by frequency (samples/s) * interval to keep track of (ms) / 1000 (ms/s) * 1.25 room for error
def calculate_max_size(sample_frequency, queue_interval):
    return floor(sample_frequency * queue_interval / 1000 * 1.25)


# Inputs: Array of functions that should be run every x ms
# 		Array of intervals of time between each run of its corresponding function
# Outputs: None
# Each function in func_arr should raise an exception if the loop should stop being run
def do_every(func_arr, interval_arr):
    prevTimes = [-999999] * len(func_arr)
    while True:
        for i, func in enumerate(func_arr):
            if time.ticks_diff(time.ticks_ms(), prevTimes[i]) > interval_arr[i]:
                try:
                    func()
                    prevTimes[i] = time.ticks_ms()
                except StopIteration:  # Leave the while loop
                    return




# NOTE: Need to close this at the end of the program
imu_data = open(get_valid_file_name("/sd/imu_data", "csv"), "w")
imu_data.write(
    "Time, Temperature, Mag X, Mag Y, Mag Z, Gyro X, Gyro Y, Gyro Z, Acc X, Acc Y, Acc Z, Lin Acc X, Lin Acc Y, Lin Acc Z, Gravity X, Gravity Y, Gravity Z, Euler X, Euler Y, Euler Z\n"
)
flight_log = open(get_valid_file_name("/sd/flight_log", "txt"), "w")




    # if time.ticks_diff(time.ticks_ms(), init_time) > 10000:
    # raise StopIteration ONLY USED FOR TESTING PURPOSES


imu_data_frequency = 100  # Hz
imu_data_interval = 1 / imu_data_frequency * 1000  # ms


# Declaring queues. They must be accessible via the global context
time_queue = None
accel_queue = None
altitude_queue = None


# Inputs: Interval: How much acceleration data should be kept track of (eg last 2000 ms, interval = 2000)
# 						NOTE: This does not mean acceleration is updated every interval ms
# Output: A function that can be passed into do_every to update the time and acceleration queues
def make_data_updater(interval):
    def updater():
        cur_time = time.ticks_ms()
        time_queue.enqueue(cur_time)
        accel_data = imu.accel()
        accel_queue.enqueue((accel_data[0] ** 2 + accel_data[1]** 2 + accel_data[2] ** 2) ** 0.5)
        altitude_queue.enqueue(pressure_sensor.altitude())
        while time.ticks_diff(cur_time, time_queue.peek()) > interval:
            time_queue.dequeue()
            accel_queue.dequeue()
    return updater



# Check for calibration every 1000 ms

do_every([calibration_fn], [1000])

# The IMU is calibrated at this point
# The reference gravity must be calculated in setup for the rest of the program to use
# For stopping the executition of program during testing
#offset_arr = bytearray(b"\xfa\xff\x00\x00\xe9\xffF\x04\x13\x01|\xff\xff\xff\x00\x00\x00\x00\xe8\x03\xec\x01")
#imu.set_offsets(offset_arr)



# -----SETUP PHASE-----
GRAVITY = 9.8
queue_frequency = 5  # Hz
check_interval = 5000  # time between variance checks

# calculate time between samples in ms based on desired frequency
accel_sample_interval = 1000 / queue_frequency
max_size = calculate_max_size(queue_frequency, check_interval)

# Queue(maximum length of queue, initial threshold)
time_queue = Queue(max_size, None)
accel_queue = Queue(max_size, GRAVITY)
data_updater = make_data_updater(check_interval)


def find_reference_gravity():  # CHECK HERE FOR SOMEWHAT ARBITRARY VALUES
    global GRAVITY
    if time.ticks_diff(time.ticks_ms(), time_queue.peek()) < check_interval * 0.5:
        return
    stats = mean_variance(accel_queue)
    if (stats[1] < 0.1 and stats[0] > 9.5 and stats[0] < 10.1):  
        # ARBITRARY: if variance less than .1 m/s^2, also check that mean is reasonable (g+-.3)
        # May also want to check that queue has big enough number of elements
        # Set reference gravity
        flight_log.write("\nCalculated Gravity: " + str(stats))
        uart.write("\nCalculated Gravity: " + str(stats))
        GRAVITY = stats[0] * 1.25 
        # ARBITRARY: Multiply by 1.1 to give some room for error
        raise StopIteration


do_every([data_updater, find_reference_gravity],[accel_sample_interval, check_interval])
# GRAVITY is set at this point
flight_log.write("\nGravity has been set: " + str(GRAVITY))
flight_log.write("\nTime (ms): " + str(time_queue.peek()))
uart.write("\n\nGravity has been calculated. Ready for flight.")
uart.write("\nGravity has been set: " + str(GRAVITY))
uart.write("\nTime (ms): " + str(time_queue.peek()))


# -----BEFORE FLIGHT PHASE-----

# Reset time and acceleration queues
queue_frequency = 50  # Hz
burn_time = 2970 * 0.85  # Multiply by .85 for some room for error
accel_sample_interval = 1000 / queue_frequency
# calculate time between samples in ms based on desired frequency
max_size = calculate_max_size(queue_frequency, burn_time)

time_queue = Queue(max_size, None)
accel_queue = Queue(max_size, GRAVITY)


def check_launch():
    if time.ticks_diff(time.ticks_ms(), time_queue.peek()) < 0.5 * burn_time:
        return  # Dont check for launch if there's not enough data in the queue yet
    uart.write("\n Launch Threshold Proportion: " + str(accel_queue.get_proportion_above_threshold()))
    if accel_queue.get_proportion_above_threshold() > 0.95:
        # ARBITRARY: If 95% of the data is above the gravity threshold, then check variance
        mean_variance_calc = mean_variance(accel_queue)
        uart.write("\n Variance of Threshold:"+str(mean_variance_calc[1]))
        if mean_variance_calc[1] > 5:  # ARBITRARY: If the variance is above 0.5 m/s^2, then launch is detected
            raise StopIteration


data_updater = make_data_updater(burn_time)
# Function to update accelerations, keeping only last burn_time ms in the queue


check_launch_interval = 1000  
# ARBITRARY: check for launch every check_launch_interval ms


do_every([write_to_imu_data, data_updater, check_launch], [imu_data_interval, accel_sample_interval, check_launch_interval])


# The rocket has launched at this point
flight_log.write("\nThe rocket has launched")
flight_log.write("\nTime (ms): " + str(time_queue.peek()))
uart.write("\n\nLaunch Detected\n")
uart.write("\nTime (ms): " + str(time_queue.peek()))


# -----IN FLIGHT PHASE-----

# Reset time and acceleration queues
queue_frequency = 25  # Hz
check_interval = 10000  # Want to keep track of last 10 seconds of acceleration data

# calculate time between samples in ms based on desired frequency
accel_sample_interval = 1000 / queue_frequency
max_size = calculate_max_size(queue_frequency, check_interval)

time_queue = Queue(max_size, None)
accel_queue = Queue(max_size, GRAVITY)


def check_landing():
    if time.ticks_diff(time.ticks_ms(), time_queue.peek()) < 0.5 * check_interval:
        return  # Dont check for landing if there's not enough data in the queue yet
    uart.write("\n Landing Threshold Proportion: " + str(accel_queue.get_proportion_above_threshold()))
    if accel_queue.get_proportion_above_threshold() > 0.95:  
        # ARBITRARY: If no more than 5% of the acceleration data is above the gravity threshold, then check variance
        uart.write("\n Variance of Threshold:" + str(mean_variance(accel_queue)[1]))
        if mean_variance(accel_queue)[1] < 0.25: 
            # ARBITRARY: If variance is below 0.25 m/s^2, then landing is detected
            raise StopIteration


data_updater = make_data_updater(check_interval)
check_landing_interval = 3000  # ARBITRARY: Check for landing every 3 seconds
do_every([write_to_imu_data, data_updater, check_landing], [imu_data_interval, accel_sample_interval, check_landing_interval])
flight_log.write("\nThe rocket has landed")
flight_log.write("\nTime (ms): " + str(time_queue.peek()))
uart.write("\n\nLanding Detected")
uart.write("\nTime (ms): " + str(time_queue.peek()))


# -----LANDED PHASE-----

# DO STUFF AFTER LANDING HERE
# Do stuff to make sure these close no matter what

servo = machine.PWM(machine.Pin(18))
servo.freq(50)  # Set PWM frequency

# define stop,CCW and CW timing in ns

# Our servo has a max ns of 2000000, min ns 1000000, and stops at ns 1500000
servoStop = 1_500_000
servoCCW = 1_450_000
servoCW = 1_550_000


def is_not_vertical():  # Checks if rocket is level since servo freaks out otherwise
    return -10 < imu.euler()[1] < 10


init_adjust_time = time.ticks_ms()


def adjust_servo_angle():
    if time.ticks_diff(time.ticks_ms(), init_adjust_time) > 10000:
        raise StopIteration
    if is_not_vertical():  # check that rocket is not moving and level
        if imu.euler()[2] > 3:  # Leveling code
            servo.duty_ns(servoCCW)
        elif imu.euler()[2] < -3:
            servo.duty_ns(servoCW)
        else:
            servo.duty_ns(servoStop)  # Tell servo to stop if the BNO is level


print("Program running...")
servo.duty_ns(servoStop)  # Servo is turned off initially

do_every([write_to_imu_data, adjust_servo_angle], [imu_data_interval, 10])
print("Done!")
servo.duty_ns(servoStop)  # Servo is turned off initially
imu_data.close()
flight_log.close()
uart.write("\n\nProgram Terminated")
