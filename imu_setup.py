import machine
from bno055 import BNO055
from bno055_base import BNO055_BASE
import time


# setup uart object (uart0 maps to pin 1 on the pico)
uart = machine.UART(0, 9600)


init_time = time.ticks_ms()

# Initialize IMU
uart.write("\nInitializing IMU\n")
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
imu = BNO055(i2c)

def write_to_imu_data():
    imu_data.write(
        str(time.ticks_diff(time.ticks_ms(), init_time) / 1000.0)
        + ","
        + str(imu.temperature())
        + ","
        + "{:5.3f},{:5.3f},{:5.3f},".format(*imu.mag())
        + "{:5.3f},{:5.3f},{:5.3f},".format(*imu.gyro())
        + "{:5.3f},{:5.3f},{:5.3f},".format(*imu.accel())
        + "{:5.3f},{:5.3f},{:5.3f},".format(*imu.lin_acc())
        + "{:5.3f},{:5.3f},{:5.3f},".format(*imu.gravity())
        + "{:4.3f},{:4.3f},{:4.3f}".format(*imu.euler())
        + "\n"
    )

# -----CALIBRATION PHASE-----
def calibration_fn():
    uart.write("Calibration required: sys {} gyro {} accel {} mag {}".format(*imu.cal_status()))
    if imu.calibrated():
        uart.write("\n\nCalibration Done!")
        flight_log.write("\nCALIBRATED!")
        # bytearray(b'\xfa\xff\x00\x00\xe9\xffF\x04\x13\x01|\xff\xff\xff\x00\x00\x00\x00\xe8\x03\xec\x01')
        raise StopIteration

print("hello world")