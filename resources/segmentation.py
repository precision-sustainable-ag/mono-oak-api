from flask_restful import Resource
from flask import make_response, send_from_directory    
import io

# from common.device_maker import CameraDevice
from common.image_collector import Collector

class Segmentation(Resource):
    def get(self, camera_id):
        c = Collector()

        local_file = c.find_file('seg' + str(camera_id))

        if local_file is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        response = make_response(send_from_directory('./images', local_file, download_name="segmentation.jpg", mimetype="image/jpeg"))

        return response
