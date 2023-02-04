import cv2
import os
import datetime
import time

call_sign = "XX4XXX"

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

image_folder = "images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

camera_index = 0
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera with index {i} is available.")
        cap.release()
        camera_index = i
        break

camera = cv2.VideoCapture(camera_index)
if camera.isOpened():
    print(f"Using camera with index {camera_index}.")
else:
    print("No camera available.")

grayscale = False

text = input("Enter codes: ")
codes = text.split()

if codes[0] != call_sign:
    print("Invalid call sign.")
    exit()

codes = codes[1:]  # remove the call sign

for code in codes:
    if code in code_to_command:
        command = code_to_command[code]
        print(f"Command given: {command}")
        # Take Image
        if code == "C3":
            time.sleep(5)
            ret, frame = camera.read()
            if ret:
                if grayscale:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_path = os.path.join(image_folder, f"image_{timestamp}.jpg")
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                cv2.imwrite(image_path, frame)
                print(f"Image taken and stored as {image_path}")
            else:
                print("Failed to take image.")
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
