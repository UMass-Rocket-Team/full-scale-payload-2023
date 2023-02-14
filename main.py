import RPi.GPIO as GPIO
from rocketTime import time_diff, get_time
from initializations import init_time, accel_queue, time_queue, altitude_queue
from controller import do_every, make_data_updater


from uart_setup import uart

uart.write("\nInitializing IMU\n")
from imu_setup import imu, write_to_imu_data, calibration_fn
uart.write("\nIMU initialized. Initializing SD Card\n")
from sd_setup import imu_data, flight_log, get_valid_file_name
uart.write("\n SD Card initialized.\n")




imu_data_frequency = 100  # Hz
imu_data_interval = 1 / imu_data_frequency * 1000  # ms

# -----CALIBRATION PHASE-----
def calibration_fn():
    uart.write("Calibration required: sys {} gyro {} accel {} mag {}".format(*imu.cal_status()))
    if imu.calibrated():
        uart.write("\n\nCalibration Done!")
        flight_log.write("\nCALIBRATED!")
        # bytearray(b'\xfa\xff\x00\x00\xe9\xffF\x04\x13\x01|\xff\xff\xff\x00\x00\x00\x00\xe8\x03\xec\x01')
        raise StopIteration


# Check for calibration every 1000 ms

do_every([calibration_fn], [1000])

# The IMU is calibrated at this point
# The reference gravity must be calculated in setup for the rest of the program to use
# For stopping the executition of program during testing
#offset_arr = bytearray(b"\xfa\xff\x00\x00\xe9\xffF\x04\x13\x01|\xff\xff\xff\x00\x00\x00\x00\xe8\x03\xec\x01")
#imu.set_offsets(offset_arr)

flight_log.write("\nIMU is calibrated")
flight_log.write("\nTime (ms): " + str(get_time()))
uart.write("\n\nIMU is calibrated")

# -----SETUP PHASE-----
GRAVITY = 9.8
ALTITUDE_THRESHOLD = 500  # ft
queue_frequency = 5  # Hz
accel_sample_interval = 1000 / queue_frequency
check_interval = 5000  # time between variance checks

data_updater = make_data_updater(queue_frequency, check_interval, (GRAVITY, ALTITUDE_THRESHOLD), (time_queue, accel_queue, altitude_queue))

def find_reference_gravity():  # CHECK HERE FOR SOMEWHAT ARBITRARY VALUES
    global GRAVITY
    if time_diff(get_time(), time_queue.peek()) < check_interval * 0.5:
        return
    mean = accel_queue.getMean()
    
    if (9.5 < mean < 10.1):
        # ARBITRARY: if variance less than .1 m/s^2, also check that mean is reasonable (g+-.3)
        # May also want to check that queue has big enough number of elements
        # Set reference gravity
        variance = accel_queue.getVariance()
        if variance < 0.1:
            flight_log.write("\nCalculated Gravity: " + str(mean))
            uart.write("\nCalculated Gravity: " + str(mean))
            GRAVITY = mean * 1.25 
            # ARBITRARY: Multiply by 1.1 to give some room for error
            raise StopIteration


do_every([data_updater, find_reference_gravity],[accel_sample_interval, check_interval])
data_updater = None

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

data_updater = make_data_updater(queue_frequency, burn_time, (GRAVITY, ALTITUDE_THRESHOLD), (time_queue, accel_queue, altitude_queue))

def check_launch():
    if time_diff(get_time(), time_queue.peek()) < 0.5 * burn_time:
        return  # Dont check for launch if there's not enough data in the queue yet
    uart.write("\n Launch Threshold Proportion: " + str(accel_queue.get_proportion_above_threshold()))
    if accel_queue.get_proportion_above_threshold() < 0.95:
        return  # ARBITRARY: If less than 95% of the data is above the gravity threshold, then the rocket has not launched
    if altitude_queue.get_proportion_above_threshold() > 0.95:
        raise StopIteration  # ARBITRARY: If more than 95% of the data is above the altitude threshold, then the rocket has launched


check_launch_interval = 1000  
# ARBITRARY: check for launch every check_launch_interval ms

do_every([write_to_imu_data, data_updater, check_launch], [imu_data_interval, accel_sample_interval, check_launch_interval])
data_updater = None

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

data_updater = make_data_updater(queue_frequency, check_interval, (GRAVITY, ALTITUDE_THRESHOLD), (time_queue, accel_queue, altitude_queue))

def check_landing():
    if time_diff(get_time(), time_queue.peek()) < 0.5 * check_interval:
        return  # Dont check for landing if there's not enough data in the queue yet
    uart.write("\n Landing Threshold Proportion: " + str(accel_queue.get_proportion_above_threshold()))
    if accel_queue.get_proportion_above_threshold() > 0.05:
        return
    # ARBITRARY: If more than 5% of the data is above the gravity threshold, then the rocket has not landed
    if altitude_queue.get_proportion_above_threshold() < 0.05:
        raise StopIteration
    # ARBITRARY: If less than 5% of the data is above the altitude threshold, then the rocket has landed


check_landing_interval = 3000  # ARBITRARY: Check for landing every 3 seconds
do_every([write_to_imu_data, data_updater, check_landing], [imu_data_interval, accel_sample_interval, check_landing_interval])
flight_log.write("\nThe rocket has landed")
flight_log.write("\nTime (ms): " + str(time_queue.peek()))
uart.write("\n\nLanding Detected")
uart.write("\nTime (ms): " + str(time_queue.peek()))

# -----AFTER FLIGHT PHASE-----
from post_landing import *

