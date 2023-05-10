from flask_restful import reqparse, Resource

# from common.device_maker import CameraDevice
from common.image_collector import Collector

parser = reqparse.RequestParser()
parser.add_argument('TypeOfCrop')
parser.add_argument('TypeOfCashCrop')
parser.add_argument('TypeOfCoverCrops')

STATUS = 'inactive'

class Status(Resource):
    def post(self, action):
        args = parser.parse_args()
        print(args)

        if action == 'start':
            STATUS = 'active'

        elif action == 'stop':
            STATUS = 'inactive'

        else:
            return {'status': 'error', 'info': 'invalid option specified. use start or stop!'}, 400
        
        return {'status': STATUS, 'args': args, 'time_elapsed': 0}, 200
