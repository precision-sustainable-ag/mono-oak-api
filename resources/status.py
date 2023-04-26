from flask_restful import Resource

# from common.device_maker import CameraDevice
from common.image_collector import Collector
STATUS = 'inactive'

class Status(Resource):
    def get(self, action):
        if action == 'start':
            STATUS = 'active'

        elif action == 'stop':
            STATUS = 'inactive'

        else:
            return {'status': 'error', 'info': 'invalid option specified. use start or stop!'}, 400
        
        return {'status': STATUS, 'time_elapsed': 0}, 200
