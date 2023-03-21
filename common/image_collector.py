import cv2
import numpy as np

class Collector():
	_shared_borg_state = {}

	def __new__(cls, *args, **kwargs):
		obj = super(Collector, cls).__new__(cls, *args, **kwargs)
		obj.__dict__ = cls._shared_borg_state
		return obj

	def initialize_queues(self, cd):
		self.preview_queue = cd.device.getOutputQueue(name="preview", maxSize=1, blocking=False)
		self.rgb_queue = cd.device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
		self.left_queue = cd.device.getOutputQueue(name="left", maxSize=1, blocking=False)
		self.right_queue = cd.device.getOutputQueue(name="right", maxSize=1, blocking=False)
		self.disparity_queue = cd.device.getOutputQueue(name="disparity", maxSize=1, blocking=False)

	def get_frame(self, queue, img_type, depth=None):
		img_out = queue.tryGet()

		if img_out is not None:
			if img_type == "depth":
				img_out = img_out.getCvFrame()
				img_out = (img_out * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
				_, img_encoded = cv2.imencode('.png', img_out)
			elif 'img_type' == 'rgb':
				img_encoded = img_out.getData()
			else:
				img_out = img_out.getCvFrame()
				encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 98]
				_, img_encoded = cv2.imencode('.jpg', img_out, encode_param)

			byte_stream = img_encoded.tobytes()

			return byte_stream

		return None
