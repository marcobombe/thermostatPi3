#!/usr/bin/python

import time
import os
import random
import subprocess
import RPi.GPIO as GPIO

playPath = '/media/pi/Transcend'
# myprocess = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

leds = {
    18: 14,
    24: 15,
    8: 25,
}

for button, led in leds.items():
    GPIO.setup(led, GPIO.OUT)  # led
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # button

def killmp3 ():
	os.system('killall omxplayer.bin')
	print('gekillt oida')
	# myprocess.terminate()def

def lookForButtons(buttonNum):
    input_state = GPIO.input(buttonNum)
    if not input_state:
        print('press '+str(buttonNum))
        # new button was pressed
        time.sleep(0.2)
	x = 1;
	while x == 1:
	    input_state = GPIO.input(buttonNum)
	    if not input_state:
		#print('x')
                time.sleep(0.2)
	    else:
                # global myprocess
		# myprocess.kill()
			x = 0
			killmp3()
			print('Button ausgeschalten')

while True:
    for key in leds:
        lookForButtons(key)
    killmp3()
    time.sleep(.05)  # don't lock the cpurndmp3()
