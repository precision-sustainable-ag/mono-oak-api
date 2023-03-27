import cv2
import numpy as np
import os, shutil

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
			sequence_number = img_out.getSequenceNum()
			print(sequence_number)

			sensitivity = img_out.getSensitivity()
			print(sensitivity)

			exposure_time = img_out.getExposureTime()
			print(exposure_time)

			if img_type == "depth":
				img_out = img_out.getCvFrame()
				img_out = (img_out * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint16)
				_, img_encoded = cv2.imencode('.png', img_out)
				cv2.imwrite('./images/{}_{}_{}_{}.png'.format(img_type, sequence_number, sensitivity, exposure_time), img_out)
			
			elif img_type == 'rgb':								
				img_encoded = img_out.getData()
				# cv2.imwrite('/images/{}.jpg'.format(img_type), img_out)
				with open("./images/{}_{}_{}_{}.jpg".format(img_type, sequence_number, sensitivity, exposure_time), "wb") as fw:
					fw.write(img_encoded)
				
			else:
				img_out = img_out.getCvFrame()
				cv2.imwrite('./images/{}_{}_{}_{}.jpg'.format(img_type, sequence_number, sensitivity, exposure_time), img_out)
				encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 98]
				_, img_encoded = cv2.imencode('.jpg', img_out, encode_param)

			byte_stream = img_encoded.tobytes()

			return byte_stream, sequence_number, sensitivity, exposure_time

		return None

	def save_frames(self, depth):
		folder = './images'
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))


		image_data = [
			{'img_type': 'depth', 'queue': self.disparity_queue},
            {'img_type': 'right', 'queue': self.right_queue}, 
            {'img_type': 'left', 'queue': self.left_queue},
            {'img_type': 'rgb', 'queue': self.rgb_queue}, 
        ]

		for data in image_data:
			print(data.get('img_type'))
			img_out = data.get('queue').tryGet()

			if img_out is not None:
				data['sequence_number'] = img_out.getSequenceNum()
				data['sensitivity'] = img_out.getSensitivity()
				data['exposure_time'] = img_out.getExposureTime()
				data['img_out'] = img_out
			else:
				data['img_out'] = None

		for data in image_data:
			print(data.get('img_type'))
			if data.get('img_type') == "depth":
				# print(depth)
				img_out = img_out.getCvFrame()
				img_out = (img_out * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint16)
				cv2.imwrite('./images/{}_{}_{}_{}.png'.format(data.get('img_type'), data.get('sequence_number'), data.get('sensitivity'), data.get('exposure_time')), img_out)
			if data.get('img_type') == 'rgb':
				with open("./images/{}_{}_{}_{}.jpg".format(data.get('img_type'), data.get('sequence_number'), data.get('sensitivity'), data.get('exposure_time')), "wb") as fw:
					fw.write(data.get('img_out').getData())
			else:
				cv2.imwrite('./images/{}_{}_{}_{}.png'.format(data.get('img_type'), data.get('sequence_number'), data.get('sensitivity'), data.get('exposure_time')), data.get('img_out').getCvFrame())
