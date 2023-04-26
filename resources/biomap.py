from flask_restful import Resource
from flask import make_response, send_from_directory    
import io

# from common.device_maker import CameraDevice
from common.image_collector import Collector

class Biomap(Resource):
    def get(self):
        c = Collector()

        local_file = c.find_file('biomap')

        if local_file is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        response = make_response(send_from_directory('./images', local_file, download_name="biomap.png", mimetype="image/png"))

        return response
