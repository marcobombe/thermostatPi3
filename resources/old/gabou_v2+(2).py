#!/usr/bin/python

# This is assuming you've followed the instructions at
# https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

# This project was created by Bob Clagett of I Like To Make Stuff
# More details and build video available at http://www.iliketomakestuff.com/

import time
import os
import random
import subprocess
import RPi.GPIO as GPIO

playPath = "/media/pi/TRANSCEND"
# Die Liste der Pins auf denen dann die Buttons verbunden sind
pins = [18,24,8]

# Die Pins die Als LEDs verwendet werden
ledPins = [14,15,25]

# Die Namen der Folder auf dem USB-Stick wo die verscbiedenen Lieder gespeichert sind
playlistNamen = ['Pl.1','Pl.2','Pl.3']

playlists = {}
leds = {}




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# on/off button auf Pin 3
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for i in range(3):
    leds[pins[i]]=ledPins[i]
    playlists[pins[i]]=playlistNamen[i]

for button, led in leds.items():
    # Initialisierung der Ledpins und der Buttons
    GPIO.setup(led, GPIO.OUT)  # led wird als OUT initialisiert
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button wird als IN intitalisiert



def showReady():
    lp = 0
    # runs a simple animation with the buttons LEDS so you know it's ready.
    while lp < 4:
        for led in leds.values():
            GPIO.output(led, True)
            time.sleep(.15)
            GPIO.output(led, False)
        lp += 1
    time.sleep(1)



def clearlights():
    for led in leds.values():
        GPIO.output(led, False)

		
def rndmp3 (playLName,buttonNum):
    x = 1
    while x == 1:
        selPath = playPath+"/"+playLName
        randomfile = random.choice(os.listdir(selPath))+""
        file = selPath +"/"+ randomfile
        # os.system ('omxplayer -o local' + file)
        # global myprocess
        # myprocess = subprocess.Popen(['omxplayer',file])
        os.system("omxplayer " + file)
        print('omx gestartet')
        time.sleep(.5)
        input_state = GPIO.input(buttonNum)
	if not input_state:
            # Wenn der Button noch gedrueckt ist
	    time.sleep(0.2)
	else:
	    # Wenn der Button nicht mehr gedrueckt ist -> prozess wird beendet
            print('Schleife beendet')
	    x = 0
	

		
		
def lookForButtons(buttonNum):
    input_state = GPIO.input(buttonNum)
    if not input_state:
        clearlights()
        print('press '+str(buttonNum))
        # new button was pressed
        GPIO.output(leds.get(buttonNum, ''), True)
        time.sleep(0.2)
        rndmp3(playlists.get(buttonNum, ''),buttonNum)
        pressed = buttonNum
	


def lookForShutDown():
    shutDownButton = GPIO.input(3)
    if not shutDownButton:
        showReady()
        GPIO.cleanup()
        os.system('shutdown now -h')


# setup complete, start running stuff
print('Musicbox is juiced up ready o/')
showReady()

while True:
    for key in leds:
        lookForButtons(key)
    lookForShutDown()
    time.sleep(.05)  # don't lock the cpu
