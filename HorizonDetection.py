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

# Canny: Edge detection through Gaussian blur and gradient calculation
# Input: img
# Output: img with edges detected
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # Convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # Blur img
    canny = cv2.Canny(blur, 50, 150) # Canny edge detection
    return canny

# Region of Interest: Crop img to only include region of interest
# Input: img, mask
# Output: img cropped to region of interest
def region_of_interest(img, mask):
    mask = cv2.bitwise_not(mask) # Invert mask
    masked_image = cv2.bitwise_and(img, mask) # Apply mask using bitwise AND
    return masked_image

# drawLines: Draw lines on img based on line parameters. 
# Only for debugging masked lines and unmasked lines.
# Input: img, lines
# Output: img with lines drawn on it
def drawLines(img, lines):
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

def drawHorizon(img, line):
    cv2.line(img, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 2)

# parameterize: Convert line parameters to slope and intercept 
# Input: Array of line lengths, array of line parameters, left index, right index
# Output: Tuple of slope and intercept
def parameterize(lines):
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
def compareHorizonCandidates(masked_lines, unmasked_lines, height, width):
    variance = height/20
    maskedParams = []
    unmaskedParams = []
    totalParams = []
    maskedAv = None
    unmaskedAv = None
    totalAv = None
    if masked_lines is not None:
        maskedParams.append(parameterize(masked_lines))
        maskedAv = np.average(maskedParams, axis=0)
    if unmasked_lines is not None:
        unmaskedParams.append(parameterize(unmasked_lines))
        unmaskedAv = np.average(unmaskedParams, axis=0)
    if unmasked_lines is not None and masked_lines is not None:
        if (unmaskedAv[1] <= maskedAv[1] + variance) and (unmaskedAv[1] >= maskedAv[1] - variance):
            totalParams.append(unmaskedParams)
            totalParams.append(maskedParams)
            totalAv = np.average(totalParams, axis=0)
            return make_coordinates(width, totalAv)
        else:
            return make_coordinates(width, maskedParams)
    elif  unmasked_lines is not None:
        return make_coordinates(width, [unmaskedAv])
    else:
        return make_coordinates(width, [maskedAv])

# make_coordinates: Convert line parameters to coordinates
# Input: Width of img, line parameters
# Output: Coordinates of line
# Note: Line parameters are in the form (slope, intercept)          
def make_coordinates(width, line_parameters):
    m, b = line_parameters[0]
    x1 = 0
    x2 = width
    y1 = int(m*x1+b)
    y2 = int(m*x2+b)
    return np.array([x1, y1, x2, y2])

# generateSkyMask: Generate a binary mask of the sky. The mask is generated by
# converting the img to black and white, blurring it, and then thresholding
# it. The threshold is determined by the Otsu method.
# Input: img
# Output: Binary mask of sky
def generateSkyMask(img):
    bw_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# Convert to BW for binary masking
    blur_image = cv2.bilateralFilter(bw_image, 20, 100, 100) # Blur For binary masking
    _, skyMask = cv2.threshold(blur_image, 250, 255, cv2.THRESH_OTSU) # Binary mask. First part of tuple is voided
    return skyMask

# rotateImg: Rotate img by angle
# Input: img, angle
# Output: Rotated img
def rotateImg(img, angle):
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    return cv2.warpAffine(img, rotation_matrix, (width, height))

# ----------
# START MAIN
# ----------

raw_img = cv2.imread('BamaRotated.jpg') # Read img
height, width = raw_img.shape[:2]
MINSCALEFACTOR = 11
img = np.copy(raw_img) # Copies img so that img is not edited when lane img is
canny_image = canny(img) # Canny edge detection
skyMask = generateSkyMask(img) # Create mask of sky
cropped_image = region_of_interest(canny_image, skyMask) # Crop non-sky
masked_lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 100, np.array([]), minLineLength=width/MINSCALEFACTOR, maxLineGap=5) # Identify straight edge within mask
unmasked_lines = cv2.HoughLinesP(canny_image, 1, np.pi/180, 100, np.array([]), minLineLength=width/MINSCALEFACTOR, maxLineGap=5) # Identify straight edge
horizon_prediction = compareHorizonCandidates(masked_lines, unmasked_lines, height, width) # Compare horizon candidates

midpoint_y = (horizon_prediction[1] + horizon_prediction[3])/2
midpoint_x = (horizon_prediction[0] + horizon_prediction[2])/2

thetaVariation = round(math.degrees(math.atan((midpoint_y - horizon_prediction[3])/(midpoint_x - horizon_prediction[2]))),2) # Calculate angle of horizon
#drawLines(img, masked_lines, "masked_lines") <- Uncomment to draw masked lines. For debugging purposes.
#drawLines(img, unmasked_lines, "unmasked_lines") <- Uncomment to draw masked lines. For debugging purposes.
drawHorizon(img, horizon_prediction)
rotated_img = rotateImg(img, thetaVariation) # Rotate img by angle of horizon

cv2.putText(img, "Th: " + str(thetaVariation), (int(width - width * 3/10), 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Display angle of horizon

cv2.imshow('Result', img) # Show img
cv2.imshow('Rotated', rotated_img) # Show rotated img
#cv2.imshow('Cropped', cropped_image) <- Uncomment to show cropped img. For debugging purposes.
#cv2.imshow('Edge', canny_image) <- Uncomment to show edge img. For debugging purposes.
cv2.waitKey(0) # Wait for keypress
cv2.destroyAllWindows() # Close windows