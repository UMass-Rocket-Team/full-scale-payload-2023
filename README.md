# Branch: Image Processing

## For deployment in ARCHIE IP in I/O handler

This branch contains all elements required for the team's filter, as well as general image formatting tools.

## [HorizonDetection](HorizonDetection.py):

This file is responsible for horizon detection onboard ARCHIE utilizing OpenCV. Implementation relies on use of the cv2 library, so import it before use.
Input: Image
Output: Image with detected horizon, Image with detected horizon and rotational correction applied

#### Example Usage:

The below code is an example of implementation for just horizon detection:

```
test = HorizonDetection('InputImage.jpg')
testIm = test.detectHorizon()
cv2.imshow('Result', testIm)
```

While this snippet is an example of rotational correction implementation:

```
test = HorizonDetection('InputImage.jpg')
test.detectHorizon()
testIm = test.rotatetoHorizon()
cv2.imshow('Result', testIm)
```

NOTE: Use the below to terminate image display commands

```
cv2.destroyAllWindows()
```

## Version Log:

#### HorizonDetection V2 (current):

* Format as class to permit import of methods

#### HorizonDetection V1:

* Canny Edge detection implemented
* Hough lines fitting implemented
* Image cropping for likely area of intrest implemented
* Rudimentary line comparison & averaging algorithm implemented
* Basic rotational correction implemented

#### TODO:


* Crop image to rotated domain (ignore deadspace)
