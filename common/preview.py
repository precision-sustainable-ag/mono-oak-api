import cv2
import numpy as np

class Previewer():
	def __init__(self, cd):
		self.cd = cd

	def initialize_queues(self):
		self.preview_queue = self.cd.device.getOutputQueue(name="preview", maxSize=1, blocking=False)
		self.rgb_queue = self.cd.device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
		self.left_queue = self.cd.device.getOutputQueue(name="left", maxSize=1, blocking=False)
		self.right_queue = self.cd.device.getOutputQueue(name="right", maxSize=1, blocking=False)
		self.disparity_queue = self.cd.device.getOutputQueue(name="disparity", maxSize=1, blocking=False)

	def get_frame(self, queue, img_type):
		img_out = queue.tryGet()

		if img_out is not None:
			img_out = img_out.getCvFrame()

			if img_type == "depth":
				img_out = (img_out * (255 / self.cd.depth.initialConfig.getMaxDisparity())).astype(np.uint8)
				_, img_encoded = cv2.imencode('.png', img_out)
			else:
				encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 98]
				_, img_encoded = cv2.imencode('.jpg', img_out, encode_param)

			byte_stream = img_encoded.tobytes()

			return byte_stream

		else:
			response = "No image!"

		return response

	def get_preview(self):
		return self.get_frame(self.preview_queue, "preview")

	def get_rgb(self):
		return self.get_frame(self.rgb_queue, "rgb")

	def get_mono_left(self):
		return self.get_frame(self.left_queue, "left")

	def get_mono_right(self):
		return self.get_frame(self.right_queue, "right")

	def get_depth(self):
		return self.get_frame(self.disparity_queue, "depth")
