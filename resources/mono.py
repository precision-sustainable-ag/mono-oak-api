from flask_restful import Resource
from flask import make_response, send_from_directory    
import io

from common.image_collector import Collector

class Mono(Resource):
    def get(self, side):
        c = Collector()
        
        if side == 'right':
            local_file = c.find_file('right')
        elif side == 'left':
            local_file = c.find_file('left')
        else:
            return {'status': 'error', 'info': 'invalid camera specified. use left or right!'}, 400

        if local_file is None:
            return {'status': 'error', 'info': 'no image!'}, 400

        response = make_response(send_from_directory('./images', local_file, download_name="mono_{}.jpg".format(side), mimetype="image/jpeg"))

        [ img_type, sequence_number, sensitivity, exposure_time ] = local_file.split('_')
        response.headers['sequence_number'] = str(sequence_number)
        response.headers['sensitivity'] = str(sensitivity)
        response.headers['exposure_time'] = str('.'.join(exposure_time.split('.')[:-1]))

        return response
