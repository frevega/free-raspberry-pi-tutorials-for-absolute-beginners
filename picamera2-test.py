from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
import time

pi_cam = Picamera2()
pi_cam.start_preview(Preview.QTGL, x = 100, y = 200, width = 1280, height = 720, transform = Transform(vflip = 1))
pi_cam.start()
pi_cam.set_controls({"AfMode": controls.AfModeEnum.Manual.Continuous})

time.sleep(10)