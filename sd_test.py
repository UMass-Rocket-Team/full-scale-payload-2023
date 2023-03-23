import os
import machine
# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(19, machine.Pin.OUT)
# Intialize SPI peripheral (start with 1 MHz)
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

# Mount filesystem
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")
#Input: path: file name including path such as "/sd/imu_data" (don't include extension or dot)
#		ext: extension such as "csv" (don't include dot)
def get_valid_file_name(path, ext):
    try:
        os.stat(path + "." + ext)
        #If os.stat doesn't have error, then the file exists, use a different name
        get_valid_file_name(path + "1", ext)#Try same name with a "1" appended to it
    except OSError:
        #file does not exist, use this file name
        return path + "." + ext

imu_data = open(get_valid_file_name("/sd/imu_data", "csv") , "w")#Need to close