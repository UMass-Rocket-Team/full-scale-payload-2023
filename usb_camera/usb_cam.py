import cv2
import os
import datetime
import time

import serial
import RPi.GPIO as GPIO

# Define XBee 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

# Wait for RAFCO transmission
no_command = True

while no_command:
    msg = ser.readline().strip().decode()
    if len(msg) == 36:
        no_command = False

# XX4XXX C3 A1 D4 C3 F6 C3 F6 B2 B2 C3

call_sign = "XX4XXX"

# Dictionary to map codes to their corresponding command
code_to_command = {
    "A1": "Turn camera 60 deg to the right",
    "B2": "Turn camera 60 deg to the left",
    "C3": "Take picture",
    "D4": "Change camera mode from color to grayscale",
    "E5": "Change camera mode back from grayscale to color",
    "F6": "Rotate image 180 deg (upside down)",
    "G7": "Special effects filter",
    "H8": "Remove all filters"
}

# Folder to store the images
image_folder = "images"

# Create the folder if it does not exist
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Find the index of the available camera
camera_index = 0
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera with index {i} is available.")
        cap.release()
        camera_index = i
        break

# Flag to track if grayscale mode is on or off
grayscale = False

# Read the input codes
# text = input("Enter codes: ")
codes = msg.split()

# Check if the call sign is correct
if codes[0] != call_sign:
    print("Invalid call sign.")
    exit()

# Remove the call sign from the codes
codes = codes[1:]

# Iterate over the codes
for code in codes:
    # Check if code is in the dictionary
    if code in code_to_command:
        command = code_to_command[code]
        print(f"Command given: {command}")
        # Turn Camera
        if code == "A1":
            # Send message to Pico
            # Turn camera 60 deg to the right
            pass
        # Take Image
        if code == "C3":
            camera = cv2.VideoCapture(camera_index)
            # Wait for 5 seconds before taking image
            time.sleep(5)
            # Read the image from the camera
            ret, frame = camera.read()
            # If image is successfully read
            if ret:
                # Convert to grayscale if grayscale mode is on
                if grayscale:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Get the current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                # Construct the image path, timestamp, and save image
                image_path = os.path.join(image_folder, f"image_{timestamp}.jpg")
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                cv2.imwrite(image_path, frame)
                print(f"Image taken and stored as {image_path}")
            else:
                print("Failed to take image.")
            camera.release()
        # Grayscale
        if code == "D4":
            grayscale = True
        # Color
        if code == "E5":
            grayscale = False
    else:
        print("Invalid code.")

camera.release() 
cv2.destroyAllWindows()
