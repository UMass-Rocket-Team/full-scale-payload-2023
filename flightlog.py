import machine
import uos
import time

# setup uart object (uart0 maps to pin 1 on the pico)
uart = machine.UART(0, 9600)
# initialize the serial connection with given parameters
uart.init(9600, parity=None, stop=1)
time.sleep(0.5)
print("code has been run.")
uart.write("Initial Transmission\n\n")
uart.write("\nRocket was connected to power\n")
uart.write("\nWaiting 3 seconds\n")
time.sleep(3)


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
uart.write("\nIMU initialized. Initializing SD Card\n")
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


uart.write("\n SD Card initialized.\n")

flight_log.write("\nIMU is calibrated")
flight_log.write("\nTime (ms): " + str(time.ticks_ms()))
uart.write("\n\nIMU is calibrated")
