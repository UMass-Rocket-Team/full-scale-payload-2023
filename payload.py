import cv2
import os
import datetime
import time

import serial
import RPi.GPIO as GPIO

from talker import Talker

'''
Author: Calista Greenway
Project: UMass Rocket Team 2023 Primary Payload (ARCHIE)
'''

class CameraController:
    def __init__(self):
        # Define GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT) # XBee

        # Initialize XBee serial communication 
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        self.camera_index = self.find_available_camera()
        self.grayscale_mode = False

    def find_available_camera(self):
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera with index {i} is available.")
                cap.release()
                return i
        return 0

    def wait_for_command(self, call_sign):
        no_command = True
        # Wait for RAFCO command from ground station
        while no_command:
            msg = self.ser.readline().strip().decode()
            codes = msg.split()
            # Verify call sign
            if len(msg) == 36:
                if codes[0] == call_sign:
                    # Remove the call sign from the codes
                    codes = codes[1:]
                    return codes

    def process_command(self, command):
        if command == "A1":
            self.turn_camera(60)
        elif command == "B2":
            self.turn_camera(-60)
        elif command == "C3":
            self.take_picture()
        elif command == "D4":
            self.grayscale_mode = True
        elif command == "E5":
            self.grayscale_mode = False
        elif command == "F6":
            self.rotate_image(180)
        elif command == "G7":
            self.apply_special_effects()
        elif command == "H8":
            self.remove_all_filters()

    def turn_camera(self, degrees):
        # Send message to Pico
        # Turn camera to the specified degrees
        pass

    def take_picture(self):
        camera = cv2.VideoCapture(self.camera_index)
        time.sleep(1)
        ret, frame = camera.read()
        if ret:
            if self.grayscale_mode:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_path = os.path.join("images", f"image_{timestamp}.jpg")
            cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.imwrite(image_path, frame)
            print(f"Image taken and stored as {image_path}")
        else:
            print("Failed to take image.")
        camera.release()

    def rotate_image(self, degrees):
        # Rotate the most recent image by the specified degrees
        pass

    def apply_special_effects(self):
        # Apply special effects to the most recent image
        pass

    def remove_all_filters(self):
        # Remove all filters from the most recent image
        pass

    def run(self):
        '''
        STARTUP / INIT PHASE
        '''
        # Send startup confirmation to XBee
        msg = "Payload Powered ON\n\nENTERING INIT \ STARTUP PHASE"
        self.ser.write(msg.encode())
        
        # Define call sign
        call_sign = "XX4XXX"

        # Initialize Pico communication
        pico = Talker()

        # Define and calibrate IMU
        # Define and calibrate altitude sensor
        # [CODE HERE]

        '''
        LAUNCH AND RECOVERY PHASE
        '''
        msg = "\nENTERING LAUNCH AND RECOVERY PHASE\n"
        self.ser.write(msg.encode())

        # Wait for launch detection
        # Wait for landing detection
        # [CODE HERE]

        '''
        DEPLOYMENT PHASE
        '''
        msg = "\nENTERING DEPLOYMENT PHASE\n"
        self.ser.write(msg.encode())

        '''
        TASK INTERPRETATION AND EXECUTION PHASE
        '''
        msg = "\nENTERING TASK INTERPRETATION AND EXECUTION PHASE\n"
        self.ser.write(msg.encode())

        # Request RAFCO from ground station
        msg = "\nSend RAFCO command now!\n"
        self.ser.write(msg.encode())

        self.wait_for_command(call_sign)

archie = CameraController()
archie.run()