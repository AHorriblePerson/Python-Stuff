import cv2
import numpy
import math

import mss.tools

import pyautogui
import keyboard

import time

##CURRENTLY IN HORIZONTAL LEFT TO RIGHT MODE
##To switch from right to left mode swap switch around the commented and uncommented stuff
#Top to bottom left as an exercise to the reader


while True:
    if keyboard.is_pressed(","):
        (x1,y1) = pyautogui.position()
        break
while True:
    if keyboard.is_pressed("."):
        (x2,y2) = pyautogui.position()
        break
while True:
    if keyboard.is_pressed("/"):
        click_location=pyautogui.position()
        break
    
center=math.floor((y1+y2)/2)
print(center)
TBS_area={"top": center, "left": x1, "width": x2-x1, "height": 1}

prev_blue_pixle_count=0

x=0
white=255
blue=33
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = TBS_area
    time_1=0
    while "Screen capturing":
        #We find the position where the white box begins so we can check when the pixle before
        #it is blue, that is when we want to click
        img = numpy.array(sct.grab(monitor))
        img = img.reshape(x2-x1,4)
        img = img[:,2]
        white_box_begin=numpy.where(img==white)[0][0]
        #white_box_end=numpy.where(img==white)[0][-1]
        print(white_box_begin)
        #print(white_box_end)
        while True:
            img = numpy.array(sct.grab(monitor))
            img = img.reshape(x2-x1,4)
            img = img[:,2]
            if img[white_box_begin-3]==blue:
                pyautogui.click(click_location)
                break
            #if img[white_box_end+3]==blue:
            #    pyautogui.click(click_location)
            #    break
