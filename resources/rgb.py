from flask_restful import Resource
from flask import make_response, send_from_directory    
import io

from common.image_collector import Collector

class RGB(Resource):
    def get(self):
        c = Collector()

        local_file = c.find_file('rgb')

        if local_file is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        response = make_response(send_from_directory('./images', local_file, download_name="rgb.jpg", mimetype="image/jpeg"))

        [ img_type, sequence_number, sensitivity, exposure_time ] = local_file.split('_')
        response.headers['sequence_number'] = str(sequence_number)
        response.headers['sensitivity'] = str(sensitivity)
        response.headers['exposure_time'] = str('.'.join(exposure_time.split('.')[:-1]))

        return response
