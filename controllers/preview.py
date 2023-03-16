import depthai as dai
import numpy as np
import json
import socket
import time
import cv2
from flask import make_response


# from controllers.pipeline import CameraDevice

class Previewer():
	def __init__(self, cd):
		self.cd = cd

	def initialize_queues(self):
		# self.preview_queue = self.cd.device.getOutputQueue(name="preview", maxSize=1, blocking=False)

		self.rgb_queue = self.cd.device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
		# self.still_queue  = self.cd.device.getOutputQueue(name="still", maxSize=1, blocking=False)

		self.left_queue = self.cd.device.getOutputQueue(name="left", maxSize=1, blocking=False)
		self.right_queue = self.cd.device.getOutputQueue(name="right", maxSize=1, blocking=False)
		self.disparity_queue = self.cd.device.getOutputQueue(name="disparity", maxSize=1, blocking=False)

	def get_frame(self, queue):
		img_out = queue.tryGet()

		print(img_out)

		if img_out is not None:
			print("Camera has frame! ", img_out)

			
			img_out = img_out.getCvFrame()
			# print(img_out.shape)
			# img_out = cv2.pyrDown(img_out)
			# print(img_out.shape)
			# img_out = cv2.pyrDown(img_out)
			# print(img_out.shape)
			# cv2.imwrite("test.png", img_out)

			print(img_out.shape)
			# img_out = cv2.merge((img_out,img_out,img_out))
			print(img_out.shape)
			cv2.imwrite("test.png", img_out)
			
			_, img_encoded = cv2.imencode('.png', img_out)
			byte_stream = img_encoded.tobytes()
			response = make_response(byte_stream)
			response.headers.set('Content-Type', 'image/png')

		else:
			response = "No image!"

		return response

	def get_preview(self):
		return self.get_frame(self.preview_queue)

	def get_rgb(self):
		return self.get_frame(self.rgb_queue)

	def get_mono_left(self):
		return self.get_frame(self.left_queue)

	def get_mono_right(self):
		return self.get_frame(self.right_queue)

	def get_depth(self):
		return self.get_frame(self.disparity_queue)


	# def get_preview_old(self, image_type):
	# 	print("starting!")

	# 	queue = self.cd.device.getOutputQueue(name=image_type, maxSize=1, blocking=False)
		
	# 	img_out = queue.tryGet()
	# 	print(img_out)
	# 	next_image = img_out
	# 	index = 0

	# 	# while next_image is not None:
	# 	# 	print(index)
	# 	# 	index += 1
	# 	# 	img_out = next_image
	# 	# 	next_image = queue.tryGet()

	# 	if img_out is not None:
	# 		print("Camera has frame! ", img_out)

	# 		img_out = img_out.getCvFrame()

	# 		# cv2.imwrite("test.png", img_out)
	# 	# with open('{}.txt'.format(image_type), 'w') as f:
	# 	# 	f.write(str(img_out))
		

	# 	# if image_type == "disparity":
	# 	# 	img_out = queue.tryGet().getCvFrame()
	# 	# 	# init_dsp = (255 / self.cd.depth.initialConfig.getMaxDisparity())
	# 	# 	# dframe = (img_out * init_dsp)
	# 	# 	cv2.imwrite("test.png", img_out)
	# 	# else:
	# 	# 	img_out = queue.tryGet().getCvFrame()
	# 	# 	cv2.imwrite("test.png", img_out)

	# 	print("encoded!")
	# 	# print(img_out)

	# 	return img_out
