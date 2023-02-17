import machine
import time
from bno055 import BNO055

# Initialize IMU
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
imu = BNO055(i2c)


