#!/usr/bin/python3

'''
#start from client machine.
ssh-keygen
#do not use any file name or passphrase
#press enters double

ssh-copy-id -i -p 3231 rock@103.110.113.54
# this is small -p but in scp command it is capital -P

#p = subprocess.Popen(["scp", "-P 3231", filename, "rock@103.110.113.54:/var/www/html/gateway/robi/images2/"])
#sts = os.waitpid(p.pid, 0)
'''

from picamera import PiCamera
from time import sleep
from datetime import datetime
import subprocess
import cv2, pandas
import os
import pprint
camera = PiCamera()
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numberingGPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be a
GPIO.setup(16, GPIO.OUT) # Set pin 10 to be a
print("Bismillahir Rahmanir Rahim")
print("HS Engineering Sensor Program_v1.01")
i=1

filename = ""

while True: # Run forever
	#if GPIO.input(10) == GPIO.HIGH:
	GPIO.output(16, GPIO.HIGH)
	sleep(3)
	print('end')
	GPIO.output(16, GPIO.LOW)
	sleep(3)
	i=i+1

