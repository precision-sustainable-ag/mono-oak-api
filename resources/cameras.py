from flask_restful import Resource
from flask import make_response, send_file    
import io

# from common.device_maker import CameraDevice
from common.image_collector import Collector

class Cameras(Resource):
    def get(self):
        # cd = CameraDevice()
        c = Collector()

        # c.save_frames(cd.depth)

        return {'status': 'success', 'cameras': [1, 2, 3]}, 200