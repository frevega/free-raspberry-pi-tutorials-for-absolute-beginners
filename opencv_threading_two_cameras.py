# import cv2
# import threading
# from picamera2 import Picamera2
# from libcamera import controls
# from time import sleep

# class CamThread(threading.Thread):
#     def __init__(self, name, cam_id):
#         threading.Thread.__init__(self, daemon = True)
#         self.name = name
#         self.cam_id = cam_id
        
#     def run(self):
#         print("Starting ", self.name)
#         cam_preview(self.name, self.cam_id)

# def cam_preview(name, cam_id):
#     pi_cam = Picamera2(cam_id)
#     pi_cam.preview_configuration.main.size = (640, 360)

#     pi_cam.preview_configuration.main.format = "RGB888"
#     pi_cam.preview_configuration.controls.FrameRate = 60 if pi_cam.camera_idx == 0 else 50
#     pi_cam.start()

#     if pi_cam.camera_idx == 0:
#         pi_cam.set_controls({"AfMode": controls.AfModeEnum.Manual.Continuous})

#     cv2.namedWindow(name)
#     while True:
#         frame = pi_cam.capture_array()
#         cv2.imshow(name, frame)
        
#         if cv2.waitKey(1) == ord("q"):
#             break

#     cv2.destroyWindow(name)

# # Create two threads as follows
# thread0 = CamThread("cam 0", 0)
# thread0.start()
# sleep(1)
# thread1 = CamThread("cam 1", 1)
# thread1.start()

# while True:
#     pass

from collections.abc import Callable
from multiprocessing import Process
from time import sleep
from typing import Any, Iterable, Mapping

class MyProcess(Process):
    def __init__(self, id):
        super(MyProcess, self).__init__()
        self.id = id

    def run(self):
        sleep(1)
        print(f"I'm the process with id: {self.id}")

if __name__ == "__main__":
    process = MyProcess(0)
    process.start()

    process.join()
    process = MyProcess(1)
    process.start()
    process.join()

# import cv2
# from picamera2 import Picamera2
# from libcamera import controls

# pi_cam = Picamera2(0)
# pi_cam.preview_configuration.main.size = (640, 360)

# pi_cam.preview_configuration.main.format = "RGB888"
# pi_cam.preview_configuration.controls.FrameRate = 60 if pi_cam.camera_idx == 0 else 50
# pi_cam.start()
# pi_cam.set_controls({"AfMode": controls.AfModeEnum.Manual.Continuous})

# name = "test0"
# cv2.namedWindow("test0")
# cam = cv2.VideoCapture(0)
# while True:
#     frame = pi_cam.capture_array()
#     cv2.imshow(name, frame)
    
#     if cv2.waitKey(1) == ord("q"):
#         break

# cv2.destroyAllWindows()
