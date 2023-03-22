from machine import Pin, PWM, I2C
from time import sleep
from bno055 import BNO055

# Initialize IMU
i2c = I2C(0, sda=Pin(16), scl=Pin(17))
imu = BNO055(i2c)

# Initialize servos
servo_xy = PWM(Pin(18))
servo_xz = PWM(Pin(19))

print(servo_xy.duty_u16())

led = Pin(25, Pin.OUT)

# Turn the LED on
def on():
    led.value(1)

# Turn the LED off
def off():
    led.value(0)

# Add more servos as needed. Can reuse the functions below for all servos.

# Set the position of the servo. pos is between 0 and 180.
def set_servo_position(servo, pos):
    duty = int((pos / 180) * 65025)
    servo.duty_u16(duty)
    sleep(0.1)
    
# Define servo rotation functions
def rotate_right(servo):
    # Duty cycle for 60 degree rotation to the right
    duty_cycle = 65535 * 0.055
    servo.duty_u16(int(duty_cycle))
    time.sleep(1)
    # Stop the servo
    servo.duty_u16(0)

def rotate_left(servo):
    # Duty cycle for 60 degree rotation to the left
    duty_cycle = 65535 * 0.095
    servo.duty_u16(int(duty_cycle))
    time.sleep(1)
    # Stop the servo
    servo.duty_u16(0)

on()
sleep(1)
off()

# Spin the servo on the x-y plane
# set_servo_position(servo_xy, 90) # set to 90 degrees
# sleep(1)
# set_servo_position(servo_xy, 180) # set to 180 degrees
# sleep(1)
# set_servo_position(servo_xy, 0) # set to 0 degrees
# sleep(1)

# print("starting")
# for i in range(0, 181, 10):
#     set_servo_position(servo_xy, i)
#     print(i)
#     sleep(1)


# Spin the servo on the x-z plane
# set_servo_position(servo_xz, 90) # set to 90 degrees
# sleep(1)
# set_servo_position(servo_xz, 0) # set to 0 degrees
# sleep(1)
# set_servo_position(servo_xz, 180) # set to 180 degrees
# sleep(1)

# Rotate right
# rotate_right(servo_xy)

servo_xy.duty_u16(int(65535 * 0.9))
sleep(10)

# Stop the servos
servo_xy.duty_u16(0)
servo_xz.duty_u16(0)
