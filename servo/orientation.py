from machine import Pin, PWM, I2C
from time import sleep
from bno055 import BNO055

IN1_PIN = 3
IN2_PIN = 2
SPEED_PIN = 4

# Define pins for controlling motor direction
IN1 = Pin(IN1_PIN, Pin.OUT)
IN2 = Pin(IN2_PIN, Pin.OUT)

# Define pin for controlling motor speed using PWM
speed = PWM(Pin(SPEED_PIN))
speed.freq(1000)  # PWM frequency

# Define maximum and minimum motor speeds
MAX_SPEED = 60000
MIN_SPEED = 30000

# Initialize IMU
i2c = I2C(0, sda=Pin(16), scl=Pin(17))
imu = BNO055(i2c)

def map_speed(speed_percentage):
    """Takes values 0-100 as input and returns PWM values for use with the motor control."""
    return MIN_SPEED + (MAX_SPEED - MIN_SPEED) * speed_percentage / 100

def spin_forward(speed):
    """Speed controlled motor spinning forward."""
    s = int(map_speed(speed))
    # speed = PWM(Pin(4))
    speed.duty_u16(s)
    IN1.low()  # Spin forward
    IN2.high()

def spin_backward(speed):
    """Speed controlled motor spinning backward."""
    s = int(map_speed(speed))
    # speed = PWM(Pin(4))
    speed.duty_u16(s)
    IN1.high()  # Spin backward
    IN2.low()

def brake():
    """Turn off the motor entirely."""
    speed.duty_u16(0)
    IN1.low()  # Stop
    IN2.low()

def is_level():
    """Checks if rocket is level."""
    return -10 < imu.euler()[1] < 10

def adjust_orientation_angle():
    """Adjusts orientation angle of the rocket."""
    if is_level():
        if imu.euler()[2] > 3:
            spin_backward(2)  # Leveling code
        elif imu.euler()[2] < -3:
            spin_forward(2)
        else:
            brake()

# Sample loop demonstrating motor speed being controlled
#for i in range(0,100):
#    sleep(0.05)
#    print(i)
#    spin_forward(i)

# Wait for a second
#sleep(1)

# Turn off the motor
#brake()

# Check and adjust orientation angle of the rocket
adjust_orientation_angle()
