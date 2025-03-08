import cv2
import numpy
import math

import mss.tools

import pyautogui
import keyboard

#Steps:
##1. press "," when cursor is over "Fight Gods" button on special panel
##2. fight through "Fight Gods" and click "." when cursor is over a red section of your own health bar
##3. click "/" when cursor is over "Finish" Panel
## After This Autobattler Will Begin Running!
## hold "x" to quit

while True:
    if keyboard.is_pressed(","):
        fight_location = pyautogui.position()
        break
while True:
    if keyboard.is_pressed("."):
        (hpx,hpy) = pyautogui.position()
        break
while True:
    if keyboard.is_pressed("/"):
        finish_location = pyautogui.position()
        break
    
hp_bar_pixle={"top": hpy, "left": hpx, "width": 1, "height": 1}

red=29
grey=42
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = hp_bar_pixle
    while "Screen capturing":
        #We find the position where the white box begins so we can check when the pixle before
        #it is blue, that is when we want to click
        img = numpy.array(sct.grab(monitor))
        img = img.reshape(1,4)
        img = img[:,0][0]
        if img==red:
            pyautogui.press(["q","w","r"])
        elif img==grey:
            pyautogui.press("0")
            pyautogui.click(finish_location)
            pyautogui.click(fight_location)
        else:
            print("error: not expected pixle, quitting")
            pyautogui.press("0")
            pyautogui.click(finish_location)
            pyautogui.click(fight_location)
