import time
import machine

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