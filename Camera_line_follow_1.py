# Core opencv code provided by Einsteinium Studios
# Revisions to work with Pi Camera v3 by Briana Bouchard

import numpy as np
import cv2
from picamera2 import Picamera2
from libcamera import controls
import time

picam2 = Picamera2() # assigns camera variable
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) # sets auto focus mode
picam2.start() # activates camera

time.sleep(1) # wait to give camera time to start up
 
def camera_val():
    # Display camera input
    image = picam2.capture_array("main")
    cv2.imshow('img',image)
    #image = cv2.rotate(image, cv2.ROTATE_180)
 
    # Crop the image
    crop_img = image[60:120, 160:320]
 
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
 
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
 
    # Color thresholding
    input_threshold,comp_threshold = cv2.threshold(blur,85,255,cv2.THRESH_BINARY_INV)
 
    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(comp_threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
 
    # Find the biggest contour (if detected)
    cx_max = 120
    cx_min = 50
    cx = 2000;
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c) # determine moment - weighted average of intensities
        if int(M['m00']) != 0:
            cx = int(M['m10']/M['m00']) # find x component of centroid location
            cx_last = cx
            cy = int(M['m01']/M['m00']) # find y component of centroid location
 
        #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1) # display vertical line at x value of centroid
        #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1) # display horizontal line at y value of centroid
 
        #cv2.drawContours(crop_img, contours, -1, (0,255,0), 2) # display green lines for all contours
         
        # determine location of centroid in x direction and adjust steering recommendation
        if cx >= cx_max:
            print("Turn Left!")
 
        if cx < cx_max and cx > cx_min:
            print("On Track!")
 
        if cx <= cx_min:
            print("Turn Right")
 
    else:
        print("I don't see the line")
        
 
    # Display the resulting frame
    #cv2.imshow('frame',crop_img)
    return cx, cx_max, cx_min
    
    # Check for "q" key press to end program
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        
