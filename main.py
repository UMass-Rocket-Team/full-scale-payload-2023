import rocket_time
import rocket_controller
import rocket_intializations

# -----INITIALIZE TIMER-----
rocket_timer = rocket_time.RocketTimer()

# -----INITIALIZE CONTROLLER-----
rocket_controller = rocket_controller.RocketController()

# -----INITIALIZE PERIPHERALS-----
# Initialize IMU
imu = rocket_intializations.RocketIMU()
# Initialize SD Card
sd = rocket_intializations.RocketSDCard()
sd_save_interval = 10000  # ms
# Initialize UART
uart = rocket_intializations.RocketRadio()
# Initialize Pressure Sensor
pressure_sensor = rocket_intializations.RocketPressureSensor()

imu_data_frequency = 100  # Hz
imu_data_interval = 1 / imu_data_frequency * 1000  # ms


# -----CALIBRATION PHASE-----
def calibration_fn():
    uart.write("Calibration required: sys {} gyro {} accel {} mag {}".format(*imu.calibration_status()))
    if imu.calibrated():
        uart.write("\n\nCalibration Done!")
        sd.write_to_flight_log("\nCALIBRATED!")
        # bytearray(b'\xfa\xff\x00\x00\xe9\xffF\x04\x13\x01|\xff\xff\xff\x00\x00\x00\x00\xe8\x03\xec\x01')
        raise StopIteration

# Check for calibration every 1000 ms
#Comment out for testing
rocket_controller.do_every([calibration_fn], [1000])

# The IMU is calibrated at this point
# The reference gravity must be calculated in setup for the rest of the program to use
# For stopping the executition of program during testing
#offset_arr = bytearray(b"\xfa\xff\x00\x00\xe9\xffF\x04\x13\x01|\xff\xff\xff\x00\x00\x00\x00\xe8\x03\xec\x01")
#imu.set_offsets(offset_arr)

sd.write_to_flight_log("\nIMU is calibrated")
sd.write_to_flight_log("\nTime (ms): " + str(rocket_timer.time_since_init_ms()))
uart.write("\n\nIMU is calibrated")

# -----SETUP PHASE-----
GRAVITY = 9.8
ALTITUDE_THRESHOLD = 500  # ft
queue_frequency = 5  # Hz
accel_sample_interval = 1000 / queue_frequency
check_interval = 5000  # time between variance checks

data_updater = rocket_controller.make_data_updater(queue_frequency, check_interval, (None, GRAVITY, ALTITUDE_THRESHOLD))

def find_reference_gravity():  # CHECK HERE FOR SOMEWHAT ARBITRARY VALUES
    global GRAVITY
    if rocket_timer.time_since_ms(rocket_controller.time_queue.peek()) < check_interval * 0.5:
        return
    mean = rocket_controller.accel_queue.getMean()
    
    if (9.5 < mean < 10.1):
        # ARBITRARY: if variance less than .1 m/s^2, also check that mean is reasonable (g+-.3)
        # May also want to check that queue has big enough number of elements
        # Set reference gravity
        variance = rocket_controller.accel_queue.getVariance()
        if variance < 0.1:
            sd.write_to_flight_log("\nCalculated Gravity: " + str(mean))
            uart.write("\nCalculated Gravity: " + str(mean))
            GRAVITY = mean * 1.25 
            # ARBITRARY: Multiply by 1.1 to give some room for error
            raise StopIteration

# Find the reference gravity
rocket_controller.do_every([data_updater, find_reference_gravity],[accel_sample_interval, check_interval])

sd.write_to_flight_log("\nGravity has been set: " + str(GRAVITY))
sd.write_to_flight_log("\nTime (ms): " + str(rocket_controller.time_queue.peek()))
uart.write("\n\nGravity has been calculated. Ready for flight.")
uart.write("\nGravity has been set: " + str(GRAVITY))
uart.write("\nTime (ms): " + str(rocket_controller.time_queue.peek()))

def find_reference_altitude():
    global ALTITUDE_THRESHOLD
    if rocket_timer.time_since_ms(rocket_controller.time_queue.peek()) < check_interval * 0.5:
        return
    mean = rocket_controller.altitude_queue.getMean()
    variance = rocket_controller.altitude_queue.getVariance()
    if variance < 10:
        sd.write_to_flight_log("\nCalculated Altitude: " + str(mean))
        uart.write("\nCalculated Altitude: " + str(mean))
        ALTITUDE_THRESHOLD = mean + 500
        # ARBITRARY: Multiply by 0.9 to give some room for error
        raise StopIteration

# Find the reference altitude
rocket_controller.do_every([data_updater, find_reference_altitude],[accel_sample_interval, check_interval])

print("Entering launch detection phase")
sd.write_to_flight_log("\nAltitude has been set: " + str(ALTITUDE_THRESHOLD))
sd.write_to_flight_log("\nTime (ms): " + str(rocket_controller.time_queue.peek()))
uart.write("\n\nAltitude has been calculated. Ready for flight.")
uart.write("\nAltitude has been set: " + str(ALTITUDE_THRESHOLD))
uart.write("\nTime (ms): " + str(rocket_controller.time_queue.peek()))
data_updater = None
#------BEFORE FLIGHT PHASE-----

# Reset time and acceleration queues
queue_frequency = 50  # Hz
burn_time = 2970 * 0.85  # Multiply by .85 for some room for error
accel_sample_interval = 1000 / queue_frequency

data_updater = rocket_controller.make_data_updater(queue_frequency, burn_time, (None, GRAVITY, ALTITUDE_THRESHOLD))

def check_launch():
    print("Checking for launch")
    print("Time since start: " + str(rocket_timer.time_since_init_ms()))
    if rocket_timer.time_since_ms(rocket_controller.time_queue.peek()) < 0.5 * burn_time:
        return  # Dont check for launch if there's not enough data in the queue yet
    uart.write("\n Launch Threshold Proportion: " + str(rocket_controller.accel_queue.get_proportion_above_threshold()))
    print("Checking accel: " + str(rocket_controller.accel_queue.get_proportion_above_threshold()))
    if rocket_controller.accel_queue.get_proportion_above_threshold() < 0.95:
        return  # ARBITRARY: If less than 95% of the data is above the gravity threshold, then the rocket has not launched
    print("Checking altitude: " + str(rocket_controller.altitude_queue.get_proportion_above_threshold()))
    if rocket_controller.altitude_queue.get_proportion_above_threshold() > 0.95:
        raise StopIteration  # ARBITRARY: If more than 95% of the data is above the altitude threshold, then the rocket has launched


check_launch_interval = 1000  
# ARBITRARY: check for launch every check_launch_interval ms

rocket_controller.do_every([sd.write_to_imu_data, data_updater, check_launch, sd.save_files], [imu_data_interval, accel_sample_interval, check_launch_interval, sd_save_interval])
data_updater = None
print("Launch detected")
# The rocket has launched at this point
sd.write_to_flight_log("\nThe rocket has launched")
sd.write_to_flight_log("\nTime (ms): " + str(rocket_controller.time_queue.peek()))
uart.write("\n\nLaunch Detected\n")
uart.write("\nTime (ms): " + str(rocket_controller.time_queue.peek()))


# -----IN FLIGHT PHASE-----

# Reset time and acceleration queues
queue_frequency = 25  # Hz
check_interval = 10000  # Want to keep track of last 10 seconds of acceleration data

# calculate time between samples in ms based on desired frequency
accel_sample_interval = 1000 / queue_frequency

data_updater = rocket_controller.make_data_updater(queue_frequency, check_interval, (None, GRAVITY, ALTITUDE_THRESHOLD))

def check_landing():
    if rocket_timer.time_since_ms(rocket_controller.time_queue.peek()) < 0.5 * check_interval:
        return  # Dont check for landing if there's not enough data in the queue yet
    print("Checking for landing")
    print("Time since start: " + str(rocket_timer.time_since_init_ms()))
    uart.write("\n Landing Threshold Proportion: " + str(rocket_controller.accel_queue.get_proportion_above_threshold()))
    print("Checking accel: " + str(rocket_controller.accel_queue.get_proportion_above_threshold()))
    if rocket_controller.accel_queue.get_proportion_above_threshold() > 0.05:
        return
    # ARBITRARY: If more than 5% of the data is above the gravity threshold, then the rocket has not landed
    print("Checking altitude: " + str(rocket_controller.altitude_queue.get_proportion_above_threshold()))
    if rocket_controller.altitude_queue.get_proportion_above_threshold() < 0.05:
        raise StopIteration
    # ARBITRARY: If less than 5% of the data is above the altitude threshold, then the rocket has landed
print("Entering landing detection phase")

check_landing_interval = 3000  # ARBITRARY: Check for landing every 3 seconds
rocket_controller.do_every([sd.write_to_imu_data, data_updater, check_landing, sd.save_files], [imu_data_interval, accel_sample_interval, check_landing_interval, sd_save_interval])
data_updater = None
print("Landing detected")
sd.write_to_flight_log("\nThe rocket has landed")
sd.write_to_flight_log("\nTime (ms): " + str(rocket_controller.time_queue.peek()))
uart.write("\n\nLanding Detected")
uart.write("\nTime (ms): " + str(rocket_controller.time_queue.peek()))

# -----AFTER FLIGHT PHASE-----
print("Post Landing Phase Would Go Here")
uart.close()
#from post_landing import *

