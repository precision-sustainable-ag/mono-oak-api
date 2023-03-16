import depthai as dai
import numpy as np
import json
import socket
import time
import cv2

class Previewer():
	def __init__(self, cd):
		self.cd = cd

	def get_preview(self, image_type):
		print("starting!")

		queue = self.cd.device.getOutputQueue(name=image_type, maxSize=2, blocking=False)
		
		img_out = queue.tryGet()

		if img_out is not None:
			print("Camera has frame! ", img_out)

			img_out = img_out.getCvFrame()
			
			cv2.imwrite("test.png", img_out)
		

		# if image_type == "disparity":
		# 	img_out = queue.tryGet().getCvFrame()
		# 	# init_dsp = (255 / self.cd.depth.initialConfig.getMaxDisparity())
		# 	# dframe = (img_out * init_dsp)
		# 	cv2.imwrite("test.png", img_out)
		# else:
		# 	img_out = queue.tryGet().getCvFrame()
		# 	cv2.imwrite("test.png", img_out)

		print("encoded!")
		# print(img_out)

		return img_out
