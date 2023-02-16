import cv2
import os
import datetime
import time

import serial
import RPi.GPIO as GPIO


class CameraController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)

        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        self.camera_index = self._find_available_camera()

        self.grayscale_mode = False

    def _find_available_camera(self):
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera with index {i} is available.")
                cap.release()
                return i
        return 0

    def _wait_for_command(self):
        no_command = True

        while no_command:
            msg = self.ser.readline().strip().decode()
            if len(msg) == 36:
                no_command = False

        return msg

    def _process_command(self, command):
        if command == "A1":
            self._turn_camera(60)
        elif command == "B2":
            self._turn_camera(-60)
        elif command == "C3":
            self._take_picture()
        elif command == "D4":
            self.grayscale_mode = True
        elif command == "E5":
            self.grayscale_mode = False
        elif command == "F6":
            self._rotate_image(180)
        elif command == "G7":
            self._apply_special_effects()
        elif command == "H8":
            self._remove_all_filters()

    def _turn_camera(self, degrees):
        # Send message to Pico
        # Turn camera to the specified degrees
        pass

    def _take_picture(self):
        camera = cv2.VideoCapture(self.camera_index)
        time.sleep(5)
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

    def _rotate_image(self, degrees):
        # Rotate the most recent image by the specified degrees
        pass

    def _apply_special_effects(self):
        # Apply special effects to the most recent image
        pass

    def _remove_all_filters(self):
        # Remove all filters from the most recent image
        pass

    def run(self):
        msg = self._wait_for_command()
        call_sign = "XX4XXX"
        codes = msg.split()

        if codes[0] != call_sign:
            print("Invalid call sign.")
            exit()

        codes = codes[1:]

        for code in codes:
            if code in code_to_command:
                command = code_to_command[code]
                print(f"Command given: {command}")
                self._process_command(code)
            else:
               pass