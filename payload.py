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
        self.upsidedown_mode = False
        self.special_mode = False

    def find_available_camera(self):
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_GSTREAMER)
            if cap.isOpened():
                print(f"Camera with index {i} is available.")
                cap.release()
                return i
        return 0

    def wait_for_command(self, call_sign):
        no_command = True
        print("Waiting for RACFO from ground station.")
        # Wait for RAFCO command from ground station
        while no_command:
            msg = self.ser.readline().strip().decode()
            codes = msg.split()
            # Verify call sign
            if len(msg) >= 6:
                if codes[0] == call_sign:
                    # Remove the call sign from the codes
                    codes = codes[1:]
                    return codes
            # print("RAFCO incomplete. Please send another message from Xbee.")

    def process_command(self, command):
        if command == "A1": # Turn camera 60 deg to the right
            self.turn_camera(60)
        elif command == "B2": # Turn camera 60 deg to the left
            self.turn_camera(-60)
        elif command == "C3": # Take picture
            self.take_picture()
        elif command == "D4": # Change camera mode from color to grayscale
            self.grayscale_mode = True
        elif command == "E5": # Change camera mode back from grayscale to color
            self.grayscale_mode = False
        elif command == "F6": # Rotate image 180 deg (upside down)
            self.upsidedown_mode = True
        elif command == "G7": # Special effects filter
            self.special_mode = True
        elif command == "H8": # Remove all filters
            self.grayscale_mode = False
            self.upsidedown_mode = False
            self.special_mode = False

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
            if self.upsidedown_mode:
                height = frame.shape[0]
                width = frame.shape[1]
                rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), 180, 1)
                frame = cv2.warpAffine(frame, rotation_matrix, (width, height))
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_path = os.path.join("images", f"image_{timestamp}.jpg")
            cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.imwrite(image_path, frame)
            print(f"Image taken and stored as {image_path}\n")
        else:
            print("Failed to take image.")
        camera.release()

    def run(self):
        '''
        STARTUP / INIT PHASE
        '''
        print("Phase 1: Start Up / Init")

        # Send startup confirmation to XBee
        msg = "Payload Powered ON\n\nENTERING INIT \ STARTUP PHASE"
        self.ser.write(msg.encode())
        
        # Define call sign
        call_sign = "XX4XXX"

        # Initialize Pico communication
        # pico = Talker()
        # pico.send('on()')
        # time.sleep(1)
        # pico.send('off()')

        # Define and calibrate IMU
        # pico.send('calibrateIMU()')
        # Define and calibrate altitude sensor
        # [CODE HERE]

        '''
        LAUNCH AND RECOVERY PHASE
        '''
        print("Phase 2: Launch and Recovery")
        msg = "\nENTERING LAUNCH AND RECOVERY PHASE\n"
        self.ser.write(msg.encode())

        # Wait for launch detection
        # Wait for landing detection
        # [CODE HERE]

        '''
        DEPLOYMENT PHASE
        '''
        print("Phase 3: Deployment")
        msg = "\nENTERING DEPLOYMENT PHASE\n"
        self.ser.write(msg.encode())

        '''
        TASK INTERPRETATION AND EXECUTION PHASE
        '''
        print("Phase 4: Task Interpretationa and Execution\n")
        msg = "\nENTERING TASK INTERPRETATION AND EXECUTION PHASE\n"
        self.ser.write(msg.encode())

        # Request RAFCO from ground station
        msg = "\nSend RAFCO now!\n"
        self.ser.write(msg.encode())

        codes = self.wait_for_command(call_sign)
        print("RAFCO Received!")

        for code in codes:
            print("Now executing command:", code)
            self.process_command(code)
        print("All commands have been executed.")

        '''
        DATA BACKUP AND ARCHIVAL PHASE
        '''
        print("Phase 5: Data Backup and Archival")
        msg = "\nDATA BACKUP AND ARCHIVAL PHASE"
        self.ser.write(msg.encode())

archie = CameraController()
archie.run()