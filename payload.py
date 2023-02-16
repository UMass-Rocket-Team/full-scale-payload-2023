import cv2
import os
import datetime
import time
import serial

import RPi.GPIO as GPIO

class CameraController:
    def __init__(self):
        self.camera_index = self.find_available_camera()
        self.grayscale = False
    
    def find_available_camera(self):
        """
        Finds the index of the available camera.

        Returns:
        int: The index of the available camera.
        """
        camera_index = 0
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera with index {i} is available.")
                cap.release()
                camera_index = i
                break
        return camera_index

    def turn_camera(self, degrees):
        """
        Turns the camera by a certain number of degrees.

        Args:
        degrees (int): The number of degrees to turn the camera.
        """
        # Send message to Pico to turn camera
        pass

    def take_picture(self):
        """
        Takes a picture using the camera and saves it to a folder.
        """
        camera = cv2.VideoCapture(self.camera_index)
        # Wait for 5 seconds before taking image
        time.sleep(5)
        # Read the image from the camera
        ret, frame = camera.read()
        # If image is successfully read
        if ret:
            # Convert to grayscale if grayscale mode is on
            if self.grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # Construct the image path, timestamp, and save image
            image_folder = "images"
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            image_path = os.path.join(image_folder, f"image_{timestamp}.jpg")
            cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.imwrite(image_path, frame)
            print(f"Image taken and stored as {image_path}")
        else:
            print("Failed to take image.")
        camera.release()

    def set_grayscale_mode(self, is_grayscale):
        """
        Sets the grayscale mode on or off.

        Args:
        is_grayscale (bool): Whether to set the grayscale mode on or off.
        """
        self.grayscale = is_grayscale

class XBeeController:
    def __init__(self, call_sign):
        self.call_sign = call_sign
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)
        self.ser = serial.Serial(
            port = '/dev/ttyS0',
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        )
        self.wait_for_rafco_transmission()

    def wait_for_rafco_transmission(self):
        """
        Waits for RAFCO transmission before continuing.
        """
        no_command = True
        while no_command:
            msg = self.ser.readline().strip().decode()
            if len(msg) == 36:
                no_command = False

    def decode_message(self, msg):
        """
        Decodes the message sent by the XBee module.

        Args:
        msg (str): The message sent by the XBee module.

        Returns:
        list: The list of
        """
