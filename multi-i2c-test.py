import adafruit_mpl3115a2
import adafruit_bno055
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import time

imu = adafruit_bno055.BNO055_I2C(busio.I2C(SCL, SDA), 0x28)
alt = adafruit_mpl3115a2.MPL3115A2(busio.I2C(SCL, SDA), address=0x60)
while True:
    print(alt.altitude) # altitude
    print(imu.acceleration)
    time.sleep(.5)