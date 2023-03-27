from flask_restful import Resource
from flask import make_response, send_file    
import io

from common.device_maker import CameraDevice
from common.image_collector import Collector

class Snapshot(Resource):
    def get(self):
        cd = CameraDevice()
        c = Collector()

        c.save_frames(cd.depth)

        return {'status': 'success'}, 200

        # image_data = [
        #     {'type': 'depth', 'queue': c.disparity_queue}, 
        #     {'type': 'right', 'queue': c.right_queue}, 
        #     {'type': 'left', 'queue': c.left_queue},
        #     {'type': 'rgb', 'queue': c.rgb_queue}, 
        # ]

        # for data in image_data:
        #     if data.get('type') == 'depth':
        #         data['byte_stream'], data['sequence_number'], data['sensitivity'], data['exposure_time'] = c.get_frame(data.get('queue'), data.get('type'), cd.depth)
        #     else:
        #         data['byte_stream'], data['sequence_number'], data['sensitivity'], data['exposure_time'] = c.get_frame(data.get('queue'), data.get('type'))

        # # if byte_stream is None:
        # #     return {'status': 'error', 'info': 'no image!'}, 400

        # # response = make_response(send_file(io.BytesIO(byte_stream), download_name="depth.png", mimetype="image/png"))
        # # response.headers['sequence_number'] = str(sequence_number)
        # # response.headers['sensitivity'] = str(sensitivity)
        # # response.headers['exposure_time'] = str(exposure_time)
            
        # return {'status': 'success'}, 200
