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

class PyMotive(object):
	def __init__(self):
		p = subprocess.Popen(["ip", "addr",  "show",  "dev", "ppp0"])
		sts = os.waitpid(p.pid, 0)
		print('IP ADDRESS::')
		#pprint.pprint(sts)
		self.filename = ""
		#camera = PiCamera()
		self.cap = None
		self.sdThresh = 10
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		#TODO: Face Detection 1

	def distMap(self, frame1, frame2):
		"""outputs pythagorean distance between two frames"""
		frame1_32 = np.float32(frame1)
		frame2_32 = np.float32(frame2)
		diff32 = frame1_32 - frame2_32
		norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
		dist = np.uint8(norm32*255)
		return dist

	def looper(self):
		#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
		modem.Dialin(modem)

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
				if stDev > sdThresh:
					print("Motion detected.. Do something!!!")
					currentTime = datetime.now()
					timestampMessage = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
					self.filename = '/home/pi/images/x00000001_%s.jpg' % timestampMessage
					cv2.imwrite(filename=self.filename, img=frame2)
					print('start')
					p = subprocess.Popen(["scp", "-P 3231", self.filename, "rock@103.110.113.54:/var/www/html/gateway/robi/images2/"])
					sts = os.waitpid(p.pid, 0)
					print('end')
				
			except Exception as e:
				print(str(e))

if __name__ == '__main__':
	motive = PyMotive()
	motive.looper()
	#motive.cap.
