from flask import Flask, send_file
from flask_restful import Resource, Api
import io

from common.image_collector import Collector
from common.device_maker import CameraDevice

from resources.status import Status
from resources.preview import Preview
from resources.rgb import RGB
from resources.depth import Depth
from resources.mono import Mono

app = Flask(__name__)
api = Api(app)

# cd = CameraDevice()
# c = Collector(cd)

api.add_resource(Status, '/status', '/status/<string:action>')
api.add_resource(Preview, '/preview')
api.add_resource(RGB, '/rgb')
api.add_resource(Depth, '/depth')
api.add_resource(Mono, '/mono', '/mono/<string:side>')

if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/')
# def index():
#   return 'Server Works!'

# @app.route('/start')
# def start():
#   cd.upload_pipeline()
#   p.initialize_queues()
#   return 'Server started!'

# @app.route('/stop')
# def stop():
#   cd.close_pipeline()
#   return 'Server stopped!'
  
# @app.route('/preview')
# def preview():
#   byte_stream = p.get_preview()
#   return send_file(io.BytesIO(byte_stream), attachment_filename="preview.png", mimetype="image/jpeg")

# #adding variables
# @app.route('/rgb')
# def rgb():
#   byte_stream = p.get_rgb()
#   return send_file(io.BytesIO(byte_stream), attachment_filename="rgb.png", mimetype="image/jpeg")

# @app.route('/depth')
# def depth():
#   byte_stream = p.get_depth()
#   return send_file(io.BytesIO(byte_stream), attachment_filename="depth.png", mimetype="image/png")

# #adding variables
# @app.route('/mono/left')
# def mono_left():
#   byte_stream = p.get_mono_left()
#   return send_file(io.BytesIO(byte_stream), attachment_filename="mono_left.png", mimetype="image/jpeg")

# @app.route('/mono/right')
# def mono_right():
#   byte_stream = p.get_mono_right()
#   return send_file(io.BytesIO(byte_stream), attachment_filename="mono_right.png", mimetype="image/jpeg")