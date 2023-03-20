from flask_restful import Resource, fields, marshal_with
from flask import send_file
import io

from common.device_maker import CameraDevice
from common.image_collector import Collector

class Mono(Resource):
    def get(self, side):
        cd = CameraDevice()
        c = Collector()
        
        if side == 'right':
            byte_stream = c.get_frame(c.right_queue, "right")
        elif side == 'left':
            byte_stream = c.get_frame(c.left_queue, "left")
        else:
            return {'status': 'error'}, 500

        return send_file(io.BytesIO(byte_stream), attachment_filename="preview.png", mimetype="image/jpeg")
        # return {'status': cd.status}, 200