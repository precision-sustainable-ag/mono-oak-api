from flask_restful import Resource, fields, marshal_with
from flask import send_file
import io

from common.device_maker import CameraDevice
from common.image_collector import Collector

class RGB(Resource):
    def get(self):
        cd = CameraDevice()
        c = Collector()
        byte_stream = c.get_frame(c.rgb_queue, "rgb")

        if byte_stream is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        return send_file(io.BytesIO(byte_stream), download_name="rgb.png", mimetype="image/jpeg")
