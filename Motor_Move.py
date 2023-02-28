
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import RPi.GPIO as GPIO
import digitalio

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

def setMotor_left(current_step, delay):
# This function provides the step sequence

    if current_step == 0:
        yellow.value = True
        red.value = False
        gray.value = True
        green.value = False
        time.sleep(delay)

    elif current_step == 1:
        yellow.value = False
        red.value = True
        gray.value = True
        green.value = False
        time.sleep(delay)

    elif current_step == 2:
        yellow.value = False
        red.value = True
        gray.value = False
        green.value = True
        time.sleep(delay)
        
    elif current_step == 3:
        yellow.value = True
        red.value = False
        gray.value = False
        green.value = True
        time.sleep(delay)

def setMotor_right(current_step, delay):
# This function provides the step sequence

    if current_step == 0:
        yellow_1.value = False
        red_1.value = True
        gray_1.value = False
        green_1.value = True
        time.sleep(delay)

    elif current_step == 1:
        yellow_1.value = True
        red_1.value = False
        gray_1.value = False
        green_1.value = True
        time.sleep(delay)

    elif current_step == 2:
        yellow_1.value = True
        red_1.value = False
        gray_1.value = True
        green_1.value = False
        time.sleep(delay)
        
    elif current_step == 3:
        yellow_1.value = False
        red_1.value = True
        gray_1.value = True
        green_1.value = False
        time.sleep(delay)



def moveSteps(right_step_number,left_step_number, speed):    
# This function tracks the number of steps remaining based on the step input and the loop cycles

    current_step = 0
    step_count = 0
    delay = 60/(steps_rev*speed) 
     
    if right_step_number >= left_step_number:
        biggest_step = right_step_number
    else:
        biggest_step = left_step_number

    while step_count <= biggest_step:
        
        if current_step >= 0 and current_step < 3:
                current_step = current_step + 1
        elif current_step == 3:
                current_step = 0
                
        if step_count <= right_step_number:
            setMotor_right(current_step, delay)
            
        if step_count <= left_step_number:
            setMotor_left(current_step, delay)
            
        step_count = step_count+1
    
