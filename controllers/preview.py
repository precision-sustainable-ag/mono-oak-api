import cv2

class Previewer():
	def __init__(self, cd):
		self.cd = cd

	def initialize_queues(self):
		self.preview_queue = self.cd.device.getOutputQueue(name="preview", maxSize=1, blocking=False)
		self.rgb_queue = self.cd.device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
		self.left_queue = self.cd.device.getOutputQueue(name="left", maxSize=1, blocking=False)
		self.right_queue = self.cd.device.getOutputQueue(name="right", maxSize=1, blocking=False)
		self.disparity_queue = self.cd.device.getOutputQueue(name="disparity", maxSize=1, blocking=False)

	def get_frame(self, queue):
		img_out = queue.tryGet()

		print(img_out)

		if img_out is not None:
			print("Camera has frame! ", img_out)

			
			img_out = img_out.getCvFrame()
			
			_, img_encoded = cv2.imencode('.png', img_out)
			byte_stream = img_encoded.tobytes()

			return byte_stream

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
