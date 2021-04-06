#!/usr/bin/python
# -*- coding: utf-8 -*-

# Basic imports of Numpy, OpenCV, Math...
import cv2
import os
import sys
import os.path
import numpy as np
import math

# Librarys to emulate key pressing
from pynput.keyboard import Key, Controller
import pynput
import time
import random



'''================= Variables and Constants ================='''
LINE_SIZE = 20
LINE_THICKNESS = 5
keys = {
    'A': pynput.keyboard.KeyCode.from_char('a'), 
    'D': pynput.keyboard.KeyCode.from_char('d'), 
    'W': pynput.keyboard.KeyCode.from_char('w'), 
    'S': pynput.keyboard.KeyCode.from_char('s'), 
}
ESC_KEY = 27 

# Mass Constants
LOWER_MASS = 3000
MID_MASS = 4000
HIGHER_MASS = 5000

# Window Parameters
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Webcam Selection
VIDEO_CAPTURE_WEBCAM = 1

# HSV Mask for Red Color
RED_LOWER_HSV = np.array([0, 200, 80])
RED_UPPER_HSV = np.array([30, 255, 255])

# HSV Mask for Cyan Color
CYAN_LOWER_HSV = np.array([70, 100, 100])
CYAN_UPPER_HSV = np.array([90, 210, 255])

''' ========================================================='''



'''Application'''

# Initialize controller
keyboard = Controller()

def getMask(img):
    # Apply masks
    red_mask = colorFilter(img, RED_LOWER_HSV, RED_UPPER_HSV)
    cyan_mask = colorFilter(img, CYAN_LOWER_HSV, CYAN_UPPER_HSV)

    mask = cv2.bitwise_or(red_mask, cyan_mask)

    mask_copy = mask.copy()
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    # Get Contours and Mass
    red_mass, red_x, red_y = drawContourFilter(mask_rgb, red_mask)
    cyan_mass, cyan_x, cyan_y = drawContourFilter(mask_rgb, cyan_mask)

    if((red_x != 0 and red_y != 0) and (cyan_x != 0 and cyan_y != 0)):
        # Draw Center of Mass
        
        drawCenterOfMass(mask_rgb, red_x, red_y, LINE_SIZE, (255, 0, 0))
        drawCenterOfMass(mask_rgb, cyan_x, cyan_y, LINE_SIZE, (255, 0, 0))

        # Draw Line
        drawLine(mask_rgb, red_x, red_y, cyan_x, cyan_y)

        # Draw Angle
        angle = getAngle(mask_rgb, (red_x, red_y), (cyan_x, cyan_y))

        # Draw Text
        writeImageText(mask_rgb, f'{angle}', (red_x, red_y))
        writeImageText(
            mask_rgb, f'Mass Red: {red_mass}', (250, 300), (0, 255, 0))
        writeImageText(
            mask_rgb, f'Mass Cyan: {cyan_mass}', (250, 350), (0, 255, 0))

        if((red_mass > LOWER_MASS) and (cyan_mass > LOWER_MASS)):
            if(angle > 12):
                print("Press: ", keys['A'])
                keyboard.release(keys['D'])
                keyboard.press(keys['A'])
                keyboard.release(keys['A'])
            elif(angle < -12):
                print("Press: ", keys['D'])
                keyboard.release(keys['A'])
                keyboard.press(keys['D'])
                keyboard.release(keys['D'])
            if((red_mass > HIGHER_MASS) and (cyan_mass > HIGHER_MASS)):
                keyboard.press(keys['W'])
                keyboard.release(keys['S'])
            if((red_mass > LOWER_MASS and red_mass < MID_MASS) and (cyan_mass > LOWER_MASS and cyan_mass < MID_MASS)):
                keyboard.press(keys['S'])
                keyboard.release(keys['W'])
        else:
            for key in keys:
                keyboard.release(key)

    return mask_rgb

def colorFilter(img_bgr, low_hsv, high_hsv):
    # Return filtered image
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask

def drawCenterOfMass(img, cX, cY, size, color):
    
    cv2.line(img, (cX - size, cY), (cX + size, cY), color, LINE_THICKNESS)
    cv2.line(img, (cX, cY - size), (cX, cY + size), color, LINE_THICKNESS)

def drawContourFilter(image, mask):
    contour, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    big = None
    big_area = 0
    cX = 0
    cY = 0

    for c in contour:
        area = cv2.contourArea(c)
        if area > big_area:
            big_area = area
            big = c

    M = cv2.moments(big)

    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawContours(image, [big], -1, [0, 255, 0], 5)

    return big_area, cX, cY

def drawLine(img, x, y, x2, y2):
    cv2.line(img, (x, y), (x2, y2), (0, 0, 255), thickness=3, lineType=8)

def writeImageText(img, text, position, color=(0, 0, 255)):
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(img, str(text), position, font, 1.2, color, 2, cv2.LINE_AA)

def getAngle(img, point1, point2):

    # Function to get angle from 3 points
    angR = math.atan2(point1[1]-point2[1], point1[0] - point2[0])  # Radians angle
    angD = round(math.degrees(angR))  # Degrees Angle

    return angD

# Webcam Initializer
def main():
    cv2.namedWindow("Color Mask")

    # Define webcam input
    
    video = cv2.VideoCapture(VIDEO_CAPTURE_WEBCAM)

    # Define window size
    
    video.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    if video.isOpened():  # try to get the first frame
        rval, frame = video.read()
    else:
        rval = False

    while rval:
        # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada
        # Pass frame for webcam image and receive treated image
        img = getMask(frame)

        cv2.imshow("Color Mask", img)
        cv2.imshow("Original", frame)
        rval, frame = video.read()
        key = cv2.waitKey(20)

        # exit on ESC
        if key == ESC_KEY:  
            break

    cv2.destroyWindow("Color Mask")
    cv2.destroyWindow("Original")
    video.release()

if __name__ == "__main__":
    main()
