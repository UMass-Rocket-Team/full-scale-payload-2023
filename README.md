# Branch: Image Processing

## For deployment in ARCHIE IP in I/O handler

This branch contains all elements required for the team's filter, as well as general image formatting tools.

## [HorizonDetection](full-scale-payload-2023/HorizonDetection.py):

This file is responsible for horizon detection onboard ARCHIE utilizing OpenCV. 
Input: Image
Output: Image with detected horizon, Image with detected horizon and rotational correction applied

#### HorizonDetection V1 (current):

* Canny Edge detection implemented
* Hough lines fitting implemented
* Image cropping for likely area of intrest implemented
* Rudimentary line comparison & averaging algorithm implemented
* Basic rotational correction implemented

#### TODO:

* Format as class to permit import of methods
* Crop image to rotated domain (ignore deadspace)
