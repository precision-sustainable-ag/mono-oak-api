from flask_restful import Resource
from flask import make_response, send_file    
import io

from common.device_maker import CameraDevice
from common.image_collector import Collector

class RGB(Resource):
    def get(self):
        cd = CameraDevice()
        c = Collector()

        byte_stream, sequence_number, sensitivity, exposure_time = c.get_frame(c.rgb_queue, "rgb")

        if byte_stream is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        response = make_response(send_file(io.BytesIO(byte_stream), download_name="rgb.jpg", mimetype="image/jpeg"))
        response.headers['sequence_number'] = str(sequence_number)
        response.headers['sensitivity'] = str(sensitivity)
        response.headers['exposure_time'] = str(exposure_time)

        return response
