from flask_restful import Resource

from common.device_maker import CameraDevice
from common.image_collector import Collector

class Status(Resource):
    def get(self, action):
        if action == 'start':
            cd = CameraDevice()
            c = Collector()
            
            if cd.status == 'inactive':
                cd.upload_pipeline()
                c.initialize_queues(cd)
                return {'status': cd.status}, 200
            else:
                return {'status': 'error', 'info': 'pipeline already uploaded!'}, 400

        elif action == 'stop':
            cd = CameraDevice()
            if cd.status == 'active':
                cd.close_pipeline()
                return {'status': cd.status}, 200
            else:
                return {'status': 'error', 'info': 'pipeline not uploaded!'}, 400

        else:
            return {'status': 'error', 'info': 'invalid option specified. use start or stop!'}, 400