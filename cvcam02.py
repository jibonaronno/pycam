#!/usr/bin/python3

import numpy as np
import cv2
import subprocess
import os
import pprint
from gprs import SerialModem as modem
from picamera import PiCamera
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numberingGPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
##GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be a
GPIO.setup(16, GPIO.OUT) # Set pin 10 to be a

class PyMotive(object):
	def __init__(self):
		modem.Dialin(modem)
		sleep(5)
		p = subprocess.Popen(["ip", "addr",  "show",  "dev", "ppp0"])
		sts = os.waitpid(p.pid, 0)
		print('IP ADDRESS::' + str(sts))
		
		#pprint.pprint(sts)
		self.filename = ""
		#camera = PiCamera()
		self.cap = None
		self.sdThresh = 10
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		#TODO: Face Detection 1

	def RestartModem(self):
		GPIO.output(16, GPIO.HIGH)
		sleep(3)
		GPIO.output(16, GPIO.LOW)
		sleep(15)
		modem.Dialin(modem)
		sleep(3)

	def distMap(self, frame1, frame2):
		try:
			"""outputs pythagorean distance between two frames"""
			frame1_32 = np.float32(frame1)
			frame2_32 = np.float32(frame2)
			diff32 = frame1_32 - frame2_32
			norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
			dist = np.uint8(norm32*255)
			return dist
		except Exception as e:
			print(str(e))

	def looper(self):
		#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
		command_retry_count = 0
		try:
			self.cap = cv2.VideoCapture(0)
		except Exception as e:
			print(str(e))

		try:
			_, frame1 = self.cap.read()
			_, frame2 = self.cap.read()
		except Exception as e:
			print(str(e))

		facecount = 0
		while(True):

			try:
				p = subprocess.Popen(["./modemip.sh"], stdout=subprocess.PIPE)
				sts = os.waitpid(p.pid, 0)
				stdout_value = p.communicate()[0]
				#print('IP ADDRESS::' + str(stdout_value))
				if b'NA' in stdout_value:
					self.RestartModem()
					continue
			except Exception as e:
				print(str(e))

			try:
				_, frame3 = self.cap.read()
				rows, cols, _ = np.shape(frame3)
				#cv2.imshow('dist', frame3)
				dist = self.distMap(frame1, frame3)

				frame1 = frame2
				frame2 = frame3

				# apply Gaussian smoothing
				mod = cv2.GaussianBlur(dist, (9,9), 0)

				# apply thresholding
				_, thresh = cv2.threshold(mod, 100, 255, 0)

				# calculate st dev test
				_, stDev = cv2.meanStdDev(mod)

				#cv2.imshow('dist', mod)
				#cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
				if stDev > self.sdThresh:
					print("Motion detected.. Do something!!!")
					currentTime = datetime.now()
					timestampMessage = currentTime.strftime("%Y.%m.%d-%H:%M:%S")
					self.filename = '/home/pi/images/x00000001_%s.jpg' % timestampMessage
					cv2.imwrite(filename=self.filename, img=frame2)
					print('start')
					p = subprocess.Popen(["scp", "-P 3231", self.filename, "rock@103.110.113.54:/var/www/html/gateway/robi/images2/"])
					sts = os.waitpid(p.pid, os.WNOHANG|os.WUNTRACED)
					while(sts == (0,0)):
						sts = os.waitpid(p.pid, os.WNOHANG|os.WUNTRACED)
						sleep(2)
						command_retry_count += 1
						if command_retry_count > 5:
							p.terminate()
							command_retry_count = 0
					print('end')
				
			except Exception as e:
				print(str(e))

if __name__ == '__main__':
	motive = PyMotive()
	motive.looper()
	#motive.cap.
