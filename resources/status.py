from flask_restful import Resource, fields, marshal_with

from common.device_maker import CameraDevice
from common.image_collector import Collector

class Status(Resource):
    def get(self, action):
        if action == 'start':
            cd = CameraDevice()
            cd.upload_pipeline()
            c = Collector()
            c.initialize_queues(cd)
            return {'status': cd.status}, 200
        elif action == 'stop':
            cd = CameraDevice()
            cd.close_pipeline()
            return {'status': cd.status}, 200
        else:
            return {'status': 'error'}, 500