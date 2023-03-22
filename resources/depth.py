from flask_restful import Resource, fields, marshal_with
from flask import send_file
import io

from common.device_maker import CameraDevice
from common.image_collector import Collector

class Depth(Resource):
    def get(self):
        cd = CameraDevice()
        c = Collector()

        byte_stream = c.get_frame(c.disparity_queue, "depth", cd.depth)

        if byte_stream is None:
            return {'status': 'error', 'info': 'no image!'}, 400
            
        return send_file(io.BytesIO(byte_stream), attachment_filename="depth.png", mimetype="image/png")
