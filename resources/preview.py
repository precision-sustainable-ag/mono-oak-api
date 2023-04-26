from flask_restful import Resource
from flask import make_response, send_from_directory    
import io

# from common.device_maker import CameraDevice
from common.image_collector import Collector

class Preview(Resource):
    def get(self, camera_id):
        c = Collector()

        local_file = c.find_file('rgb' + str(camera_id))

        if local_file is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        response = make_response(send_from_directory('./images', local_file, download_name="preview.jpg", mimetype="image/jpeg"))

        return response
