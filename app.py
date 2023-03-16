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

@app.route('/snapshot')
def snapshot():
  return 'Here\'s a snapshot!'
  
@app.route('/preview')
def preview():
  return p.get_preview()

#adding variables
@app.route('/rgb')
def rgb():
  return p.get_rgb()

@app.route('/depth')
def depth():
  return p.get_depth()

#adding variables
@app.route('/mono/left')
def mono_left():
  return p.get_mono_left()

@app.route('/mono/right')
def mono_right():
  return p.get_mono_right()

#adding variables
@app.route('/user/<username>')
def show_user(username):
  #returns the username
  return 'Here\'s a right image!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
  #returns the post, the post_id should be an int
  return str(post_id)