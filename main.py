#Main code for ARCHIE, Raspberry Pi Pico Motor Controller & Datalogger

from machine import Pin, PWM, I2C
from time import sleep
import utime
from bno055 import *

m1 = [PWM(Pin(2)), PWM(Pin(3))] # Motor m1, pins IN1 and IN2 are connected to pins 2 and 3
m2 = [PWM(Pin(4)), PWM(Pin(5))] # Motor m2, pins ...
m3 = [PWM(Pin(6)), PWM(Pin(7))] # ...

sA = PWM(Pin(25)) # Servo PWM pin connected to pin 25
sB = PWM(Pin(24)) # Servo PWM ...

#define stop, CCW and CW timing in ns for servo motors
servoSTOP= 1500000
servoCCW = 1000000
servoCW = 2000000

i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
imu = BNO055(i2c)
calibrated = True
ignore_calibration_warning = True # CHANGE TO TRUE TO DISABLE FAILED CALIBRATION WARNING

cs = machine.Pin(19, machine.Pin.OUT)
spi = machine.SPI(1,
                  baudrate=9600,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(20),
                  mosi=machine.Pin(21),
                  miso=machine.Pin(18))

# Initialize SD card
sd = sdcard.SDCard(spi, cs)
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")
flight_log = open(get_valid_file_name("/sd/flight_log", "txt"), "w")
# Motor Control Functions
# minspeed is zero, maxspeed is 65025
def spin_forward(motor, speed):
    motor[0].freq(1000)
    motor[1].freq(1000)
    motor[0].duty_u16(speed)
    motor[1].duty_u16(0)
    sleep(0.0001)
    
def spin_backward(motor, speed):
    motor[0].freq(1000)
    motor[1].freq(1000)
    motor[0].duty_u16(0)
    motor[1].duty_u16(speed)
    sleep(0.0001)
    
def brake(motor):
    motor[0].freq(1000)
    motor[1].freq(1000)
    motor[0].duty_u16(0)
    motor[1].duty_u16(0)
    sleep(0.0001)
# ==== test code
def demo_motor_loop(): # Demo function for controlling a motor. Remove after adding own implementation of motor control   
    spin_forward(m1, 65025)
    sleep(1)
    spin_backward(m1, 65025)
    sleep(1)
    brake(m1)
# ==== end test code


# Servo Control Functions
def rotate_CCW(servo):
    servo.freq(50)
    servo.duty_ns(servoCCW)
    
def rotate_CW(servo):
    servo.freq(50)
    servo.duty_ns(servoCW)
    
def rotate_STOP(servo):
    servo.freq(50)
    servo.duty_ns(servoSTOP)
# ==== test code
def demo_servo_rotation(): # Demo function for controlling a servo
    rotate_CW(sA)
    sleep(1)
    rotate_CCW(sA)
    sleep(1)
    rotate_STOP(sA)
# ==== end code


# IMU interfacing functions
def calibration_check():
    sleep(0.1)
    if not calibrated:
        calibrated = imu.calibrated()
        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
        
def get_temp(): # Returns an integer, indicating the temperature of the IMU in C
    #calibration_check()
    return imu.temperature()

def get_mag(): # Returns a tuple with magnetometer data, in format [x, y, z]
    return imu.mag()

def get_gyro(): # Returns a tuple with gyroscope data, in format [x, y, z]
    return imu.gyro()

def get_accel(): # Returns a tuple with acceleration data, in format [x, y, z]
    return imu.accel()

def get_lin_acc(): # Returns a tuple with linear acceleration data, in format [x, y, z]
    return imu.lin_acc()

def get_gravity(): # Returns a tuple with gravity data, in format [x, y, z]
    return imu.gravity()

def get_heading(): # Returns a tuple with heading data, in format [x, y, z]
    return imu.euler()

# ==== test code
def imu_demo(): # Demo function printing out everything the IMU can measure
    sleep(0.1)
    print('Temperature {}°C'.format(imu.temperature()))
    print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
    print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
    print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
# ==== end test code

# SD Card Module Functions
