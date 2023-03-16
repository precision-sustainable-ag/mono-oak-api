from flask import Flask, send_file, make_response
import cv2
# from preview import Preview
app = Flask(__name__)

from controllers.preview import Previewer
from controllers.pipeline import CameraDevice
# from controllers.rgb import RGB
# from controllers.mono_left import MonoLeft

cd = CameraDevice()
p = Previewer(cd)
# rgb = RGB(cd)
# l = MonoLeft(cd)

def capture_image(image_type):
  print("making buffer!")
  byte = p.get_preview(image_type)
  print(byte)
  print("got bytes!")
  _, img_encoded = cv2.imencode('.png', byte)
  print("buffer made!")
  byte_stream = img_encoded.tobytes()
  # print(byte_stream)

  response = make_response(byte_stream)
  response.headers.set('Content-Type', 'image/png')

  return response

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/start')
def start():
  cd.upload_pipeline()
  return 'Server started!'

@app.route('/stop')
def stop():
  cd.close_pipeline()
  return 'Server stopped!'

@app.route('/snapshot')
def snapshot():
  return 'Here\'s a snapshot!'
  
@app.route('/preview')
def preview():
  return capture_image("preview")

#adding variables
@app.route('/rgb')
def rgb():
  return capture_image("rgb")

@app.route('/depth')
def depth():
  return capture_image("disparity")

#adding variables
@app.route('/mono/left')
def mono_left():
  return capture_image("left")

@app.route('/mono/right')
def mono_right():
  return capture_image("right")

#adding variables
@app.route('/user/<username>')
def show_user(username):
  #returns the username
  return 'Here\'s a right image!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
  #returns the post, the post_id should be an int
  return str(post_id)