from flask import Flask, render_template, Response

from PIL import Image
from StringIO import StringIO

import pygame.camera
import pygame.image

from pygame import Surface

STREAM_URL = 'http://192.168.1.87:8080/?action=stream'

RESOLUTION = (1280, 720)

app = Flask(__name__)

@app.route('/')
def stream():
    return render_template('index.html')

def gen(cam):
    surface = Surface(RESOLUTION)
    while True:
        img = cam.get_image(surface)
        data = pygame.image.tostring(img, "RGBA")
        img = Image.fromstring('RGBA', RESOLUTION, data)
        zdata = StringIO()
        img.save(zdata, 'JPEG')
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + zdata.getvalue() + b'\r\n')

cam = None

@app.route('/video_feed')
def video_feed():
    global cam

    if not cam:
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], RESOLUTION)
        cam.start()

    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    pygame.camera.init()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
