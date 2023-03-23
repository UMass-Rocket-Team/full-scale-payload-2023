# ==============================================================================
# Description: This program detects the horizon in an img using the Canny edge
# detection algorithm. It then uses the Hough transform to detect lines in the
# img. The img is then cropped to only include the region of interest, and 
# hough lines are detected again. The two sets of lines are compared, and the
# horizon is determined by the frequency of the line placement. The horizon is
# then drawn on the img.
# ==============================================================================
# Author: Mitchell Sylvia
# Date: 10/30/2018
# ==============================================================================
# Input: img
# Output: img with horizon drawn on it
# ==============================================================================

import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

class HorizonDetection:
    def __init__(self, imgName, minScaleFactor=9):
        self.MINSCALEFACTOR = minScaleFactor
        self.img = cv2.imread(imgName) # Read img
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        self.thetaVariation = 0
        self.horizon_prediction = [0, 0, 0, 0]

    def detectHorizon(self):
        height = self.height
        width = self.width
        aspectRatio = width/height
        scaledWidth=400
        scaledHeight=int(400/aspectRatio)
        scaleFactor = height/scaledHeight
        MINSCALEFACTOR = self.MINSCALEFACTOR
        resize = cv2.resize(self.img, (scaledWidth, scaledHeight))
    
        #raw_img = np.copy(self.img) # Copies img so that img is not edited when lane img is
        canny_image = self.canny(resize) # Canny edge detection
        cv2.imshow('canny', canny_image)
        unmasked_lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 100, np.array([]), minLineLength=scaledWidth/MINSCALEFACTOR, maxLineGap=5) # Identify straight edge

        self.horizon_prediction = self.compareHorizonCandidates(unmasked_lines, scaleFactor, height, width) # Compare horizon candidates

        midpoint_y = (self.horizon_prediction[1] + self.horizon_prediction[3])/2
        midpoint_x = (self.horizon_prediction[0] + self.horizon_prediction[2])/2

        self.thetaVariation = round(math.degrees(math.atan((midpoint_y - self.horizon_prediction[3])/(midpoint_x - self.horizon_prediction[2]))),2) # Calculate angle of horizon
        self.drawLines(resize, unmasked_lines) #<- Uncomment to draw masked lines. For debugging purposes.
        self.drawHorizon(self.img, self.horizon_prediction)
        
        cv2.putText(self.img, str(self.thetaVariation), (int(width - width * 1/5), int(height * 1/20)), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 15) # Display angle of horizon
        return self.img
        
    
    def rotatetoHorizon(self):
        rotated_img = self.rotateImg(self.img, self.thetaVariation) # Rotate img by angle of horizon
        cv2.imshow('Rotated', rotated_img) # Show rotated img
        return rotated_img
    
    # ==============================================================================
    # HELPER FUNCTIONS. NOT FOR CALLING EXTERNALLY.
    # ==============================================================================

    # Canny: Edge detection through Gaussian blur and gradient calculation
    # Input: img
    # Output: img with edges detected
    def canny(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # Convert to grayscale
        blur = cv2.GaussianBlur(gray, (11, 11), 0) # Blur img
        denoise = cv2.fastNlMeansDenoising(blur, 5, 21, 7)
        cv2.imshow('denoise', denoise)
        #_, binary = cv2.threshold(denoise, 1000, 255, cv2.THRESH_OTSU)
        binary = cv2.adaptiveThreshold(denoise,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3)
        blur2 = cv2.GaussianBlur(binary, (3, 3), 0)
        cv2.imshow('Contrast', blur2)
        canny = cv2.Canny(blur2, 50, 150) # Canny edge detection
        return canny

    # drawLines: Draw lines on img based on line parameters. 
    # Only for debugging masked lines and unmasked lines.
    # Input: img, lines
    # Output: img with lines drawn on it
    def drawLines(self, img, lines):
        if lines is not None:
            for line in lines:
                width = img.shape[1] # Get width of img
                x1, y1, x2, y2 = line[0] # Get line parameters
                if y1 != y2:  # Prevent division by zero
                    m = (y2-y1)/(x2-x1) # Calculate slope
                else:
                    m=0 # Prevent division by zero
                
                b = y1 - m*x1 # Calculate intercept
                cv2.line(img, (0, math.floor(b)), (width, math.floor(m*width+b)), (0, 0, 255), 2) # Draw line on img
        else:
            print("Fatal Error: No Lines Found")

    def drawHorizon(self, img, line):
        cv2.line(img, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 20)

    # parameterize: Convert line parameters to slope and intercept 
    # Input: Array of line lengths, array of line parameters, left index, right index
    # Output: Tuple of slope and intercept
    def parameterize(self, lines):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            return (slope, intercept)

    # compareHorizonCandidates: Compare the two sets of lines detected in the img.
    # The two sets of lines are compared by their slope and intercept. The individual lines are
    # then compared by their frequency of occurrence. The lines with the highest frequency
    # are then averaged to determine the horizon.
    # Input: Masked lines, unmasked lines, height of img, width of img
    # Output: Coordinates of horizon
    # Note: Line parameters are in the form (slope, intercept)
    def compareHorizonCandidates(self, unmasked_lines, scaleFactor, height, width):
        unmaskedParams = []
        unmaskedAv = None
        if unmasked_lines is not None:
            unmaskedParams.append(self.parameterize(unmasked_lines))
            unmaskedAv = np.average(unmaskedParams, axis=0)
            return self.make_coordinates(width, scaleFactor, [unmaskedAv])
        else:
            print("Fatal Error: No lines detected")

    # make_coordinates: Convert line parameters to coordinates
    # Input: Width of img, line parameters
    # Output: Coordinates of line
    # Note: Line parameters are in the form (slope, intercept)          
    def make_coordinates(self, width, scaleFactor, line_parameters):
        m, b = line_parameters[0]
        x1 = 0
        x2 = width
        y1 = int(m*x1+(scaleFactor*b))
        y2 = int(m*x2+(scaleFactor*b))
        return np.array([x1, y1, x2, y2])


    # rotateImg: Rotate img by angle
    # Input: img, angle
    # Output: Rotated img
    def rotateImg(self, img, angle):
        height = self.height
        width = self.width
        rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
        return cv2.warpAffine(img, rotation_matrix, (width, height))
