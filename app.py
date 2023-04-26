from flask import Flask, send_file
from flask_restful import Resource, Api
import io

from common.image_collector import Collector
# from common.device_maker import CameraDevice

from resources.biomap import Biomap
from resources.cameras import Cameras
from resources.preview import Preview
from resources.segmentation import Segmentation
from resources.status import Status

def register_endpoints(api):
  api.add_resource(Biomap, '/biomap', '/biomap')
  api.add_resource(Cameras, '/cameras')
  api.add_resource(Preview, '/preview', '/preview/<string:camera_id>')
  api.add_resource(Segmentation, '/segmentation', '/segmentation/<string:camera_id>')
  api.add_resource(Status, '/status', '/status/<string:action>')

def create_app(debug=True):
    # Create app
    app = Flask(__name__)

    # Create api
    api = Api(app)

    register_endpoints(api)

    return app
