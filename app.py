from flask import Flask, send_file, make_response
import cv2
import io
# from werkzeug import FileWrapper

from controllers.preview import Previewer
from controllers.pipeline import CameraDevice

app = Flask(__name__)

cd = CameraDevice()
p = Previewer(cd)

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/start')
def start():
  cd.upload_pipeline()
  p.initialize_queues()
  return 'Server started!'

@app.route('/stop')
def stop():
  cd.close_pipeline()
  return 'Server stopped!'
  
@app.route('/preview')
def preview():
  byte_stream = p.get_preview()
  return send_file(io.BytesIO(byte_stream), attachment_filename="preview.png", mimetype="image/png")

#adding variables
@app.route('/rgb')
def rgb():
  byte_stream = p.get_rgb()
  return send_file(io.BytesIO(byte_stream), attachment_filename="rgb.png", mimetype="image/png")

@app.route('/depth')
def depth():
  byte_stream = p.get_depth()
  return send_file(io.BytesIO(byte_stream), attachment_filename="depth.png", mimetype="image/png")

#adding variables
@app.route('/mono/left')
def mono_left():
  byte_stream = p.get_mono_left()
  return send_file(io.BytesIO(byte_stream), attachment_filename="mono_left.png", mimetype="image/png")

@app.route('/mono/right')
def mono_right():
  byte_stream = p.get_mono_right()
  return send_file(io.BytesIO(byte_stream), attachment_filename="mono_right.png", mimetype="image/png")