import serial
# import pico.example as pico

ser = serial.Serial("/dev/ttyACM0", 115200)
while True:
    message = "Hello World!"
    ser.write(message.encode())
ser.close()