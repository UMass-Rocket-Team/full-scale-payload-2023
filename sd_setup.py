import machine
import sdcard
import uos
from imu_setup import imu
from initializations import init_time
from rocket_time import time_diff, get_time

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(9, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(
    1,
    baudrate=10000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=machine.SPI.MSB,
    sck=machine.Pin(10),
    mosi=machine.Pin(11),
    miso=machine.Pin(8),
)
# Initialize SD card
sd = sdcard.SDCard(spi, cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

# Find a file name so nothing is overridden
def get_valid_file_name(path, ext):
    try:
        # If uos.stat doesn't have error, then the file exists, use a different name
        uos.stat(path + "." + ext)
        # Try same name with a "1" appended to it
        return get_valid_file_name(path + "1", ext)
    except OSError:
        # file does not exist, use this file name
        return path + "." + ext

# NOTE: Need to close this at the end of the program
imu_data = open(get_valid_file_name("/sd/imu_data", "csv"), "w")
imu_data.write(
    "Time, Temperature, Mag X, Mag Y, Mag Z, Gyro X, Gyro Y, Gyro Z, Acc X, Acc Y, Acc Z, Lin Acc X, Lin Acc Y, Lin Acc Z, Gravity X, Gravity Y, Gravity Z, Euler X, Euler Y, Euler Z\n"
)
flight_log = open(get_valid_file_name("/sd/flight_log", "txt"), "w")


def write_to_imu_data():
    format_str = "{:5.3f},{:5.3f},{:5.3f},"
    imu_data.write(
        str(time_diff(get_time(), init_time) / 1000.0)
        + ","
        + str(imu.temperature())
        + ","
        + format_str.format(*imu.mag())
        + format_str.format(*imu.gyro())
        + format_str.format(*imu.accel())
        + format_str.format(*imu.lin_acc())
        + format_str.format(*imu.gravity())
        + format_str.format(*imu.euler())
        + "\n"
    )

