
import time
import board
import RPi.GPIO as GPIO
import digitalio
from libcamera import controls
from picamera2 import Picamera2 
import cv2 as cv2

# Initialize pins using BCM mode (GPIO pin numbers not board numbers)
yellow = digitalio.DigitalInOut(board.D23)
yellow.direction = digitalio.Direction.OUTPUT
red = digitalio.DigitalInOut(board.D24)
red.direction = digitalio.Direction.OUTPUT
gray = digitalio.DigitalInOut(board.D10)
gray.direction = digitalio.Direction.OUTPUT
green = digitalio.DigitalInOut(board.D9)
green.direction = digitalio.Direction.OUTPUT

yellow_1 = digitalio.DigitalInOut(board.D16)
yellow_1.direction= digitalio.Direction.OUTPUT
red_1 = digitalio.DigitalInOut(board.D20)
red_1.direction = digitalio.Direction.OUTPUT
gray_1 = digitalio.DigitalInOut(board.D21)
gray_1.direction = digitalio.Direction.OUTPUT
green_1 = digitalio.DigitalInOut(board.D26)
green_1.direction = digitalio.Direction.OUTPUT

#direction values
cw = 1
ccw = 0
steps_rev = 200

error = 0
error_sum = 0
previous_error = 0
Kp = 1.5
Kd = 0.8
Ki = 0.2
PID = 0
default_step = 5
right_motor_step = 0
left_motor_step = 0

from color_mask import mask
from Camera_line_follow import camera_val
from Motor_Move import moveSteps

picam2 = Picamera2()
picam2.start() #must start the camera before taking any images
    
try:
    while(True):
        time.sleep(0.1)
        mask_array = mask(picam2)
        cv2.imshow('frame',mask_array)
        cam_info = camera_val(mask_array)
        #print("function return:",cam_info)
        cx = cam_info[0]
        cx_max = cam_info[1]
        cx_min = cam_info[2]
        
        if cx == 2000:
            error = previous_error
        elif cx >= cx_max:
            error = cx - cx_max
            
        elif cx <= cx_min:
            error = (cx - cx_min)
                
        else:
            error = 0;
        
        P = error * Kp
        
        error_sum = error_sum + error
            
        I = error_sum*Ki #Integral Controller
        #print(I)
            
        D = (error - previous_error)*Kd
        #print(D)
            
        PID = P + I + D
        PID = round(PID/25)
        print("PID:", PID)
        
        previous_error = error
        
        if PID >= default_step:
            PID = default_step
        elif PID <= -default_step:
            PID = -default_step
            
        right_motor_step = default_step + PID
        left_motor_step = default_step - PID
            
        moveSteps(right_motor_step,left_motor_step,20)
        
        #print("PID:", PID)
    
except KeyboardInterrupt:
    # Turn off GPIO pins
    GPIO.cleanup()
