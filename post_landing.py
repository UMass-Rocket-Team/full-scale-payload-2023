import machine
import time
from archive.imu_setup import imu
from archive.uart_setup import uart
from rocket_controller import do_every

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
