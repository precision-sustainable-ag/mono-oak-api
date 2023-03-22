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
            return {'status': 'error', 'info': 'invalid camera specified. use left or right!'}, 400

        if byte_stream is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        return send_file(io.BytesIO(byte_stream), download_name="mono_{}.png".format(side), mimetype="image/jpeg")
