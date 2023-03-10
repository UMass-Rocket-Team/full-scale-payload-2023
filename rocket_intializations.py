# Import libraries
import os
#from bno055 import BNO055 #Uncomment when using actual IMU
import rocket_time
from time import sleep
import simulated_data
from singleton import Singleton
import adafruit_bno055
import adafruit_mpl3115a2
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
class RocketIMU(metaclass=Singleton):
    def __init__(self):
        # Initialize IMU
        self.imu = adafruit_bno055.BNO055_I2C(busio.I2C(SCL, SDA), 0x28)
        #FOR TESTING
        #self.rocket_timer = rocket_time.RocketTimer()
        #self.sim_data = simulated_data.DataSimulator()
    def accel(self):
        return self.imu.acceleration
    def mag(self):
        return self.imu.magnetic
    def gyro(self):
        return self.imu.gyro
    def temperature(self):
        return self.imu.temperature
    def gravity(self):
        return self.imu.gravity
    def lin_acc(self):
        return self.imu.linear_acceleration
    
        
class RocketPressureSensor(metaclass=Singleton):
    def __init__(self):
        # Initialize Pressure Sensor
        self.pressure_sensor = adafruit_mpl3115a2.MPL3115A2(busio.I2C(SCL, SDA), address=0x60)
        #FOR TESTING
        #self.rocket_timer = rocket_time.RocketTimer()
        #self.sim_data = simulated_data.DataSimulator()
    def altitude(self):
        return self.pressure_sensor.altitude
class RocketRadio(metaclass=Singleton):
    def __init__(self):
        # # setup uart object (uart0 maps to pin 1 on the pico)
        # self.uart = machine.UART(0, 9600)
        # # initialize the serial connection with given parameters
        # self.uart.init(9600, parity=None, stop=1)
        # time.sleep(0.05)
        # self.uart.write("Initial Transmission\n\n")
        # self.uart.write("\nRocket was connected to power\n")
        # self.uart.write("\nWaiting 3 seconds\n")
        # time.sleep(3)
        
        #TESTING ONLY
        #Create a txt file assigned to self.uart
        self.uart = open(get_valid_file_name(r'sd/uart.txt'), "w")
    def write(self, message):
        self.uart.write(message)
    def close(self):#Only for testing purposes
        self.uart.close()
def get_valid_file_name(path_no_ext):
    #Split path into path and extension
    path, ext = os.path.splitext(path_no_ext)
    def get_valid_file_name_helper(num):
        # Check if file path+num+ext exists
        full_path = path + str(num).zfill(5) + ext
        if not os.path.exists(full_path):
            #return path with 5 digits using leading zeros
            return full_path
        # If file exists, increment num and try again
        return get_valid_file_name_helper(num+1)
    return get_valid_file_name_helper(0)

class RocketSDCard(metaclass=Singleton):
    def __init__(self):
        # # Initialize SD Card
        # self.sd = machine.SDCard(slot=1, width=1, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(20))
        # self.vfs = machine.VfsFat(self.sd)
        # machine.mount(self.vfs, "/sd")

        #TESTING ONLY
        self.files_dictionary = {}
        self.imu_data_path = r'sd/imu_data.csv'
        self.flight_log_path = r'sd/flight_log.txt'
        self.files_dictionary[self.imu_data_path] = open(get_valid_file_name(self.imu_data_path), "w")
        self.files_dictionary[self.imu_data_path].write("Time, Temperature, Mag X, Mag Y, Mag Z, Gyro X, Gyro Y, Gyro Z, Acc X, Acc Y, Acc Z, Lin Acc X, Lin Acc Y, Lin Acc Z, Gravity X, Gravity Y, Gravity Z, Euler X, Euler Y, Euler Z\n")
        self.files_dictionary[self.flight_log_path] = open(get_valid_file_name(self.flight_log_path), "w")

        self.imu = RocketIMU()
        self.rocket_timer = rocket_time.RocketTimer()
    def write_to_imu_data(self):
        format_str = "{:5.3f},{:5.3f},{:5.3f},"
        self.files_dictionary[self.imu_data_path].write(
            str(self.rocket_timer.time_since_init_ms())
            + ","
            + str(self.imu.temperature())
            + ","
            + format_str.format(*self.imu.mag())
            + format_str.format(*self.imu.gyro())
            + format_str.format(*self.imu.accel())
            + format_str.format(*self.imu.lin_acc())
            + format_str.format(*self.imu.gravity())
        )
    def write_to_flight_log(self, message):
        self.files_dictionary[self.flight_log_path].write(message)
    def save_files(self):
        for file in self.files_dictionary:
            self.files_dictionary[file].close()
            self.files_dictionary[file] = open(get_valid_file_name(file), "w")
        
    def close_files(self):
        for file in self.files:
            file.close()
