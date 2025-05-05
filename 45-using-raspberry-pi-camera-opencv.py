import cv2
from picamera2 import Picamera2
from libcamera import Transform
from time import time, sleep

print("Info:", Picamera2.global_camera_info())

pi_cam = Picamera2(camera_num=1)
# pi_cam.preview_configuration.main.size = (1920, 1080) # 22-23 @30-60-75-120 Pi5
# pi_cam.preview_configuration.main.size = (1280, 720) # 30-31 @30 // 55 @55 // 49-57 @60 // 49-60 @75 // 59-60 @120 Pi5
pi_cam.preview_configuration.main.size = (854, 480) # 60 @60 // 111 @120 Pi5
pi_cam.preview_configuration.main.format = "RGB888"
pi_cam.preview_configuration.controls.FrameRate = 120
pi_cam.preview_configuration.transform = Transform(vflip = 1)
# pi_cam.preview_configuration.align()
# pi_cam.configure("preview")
pi_cam.start()
# pi_cam.set_controls({"AfMode": controls.AfModeEnum.Manual.Continuous})

fps = 0

def get_fps(event):
    while True:
        if event.is_set():
            print("exit thread...")
            break
        print(fps, end = "\r")
        sleep(.1)

x_pos = pi_cam.preview_configuration.main.size[0] - 200

while True:
    start_time = time()
    frame = pi_cam.capture_array()
    cv2.putText(frame, f"{fps:.0f} FPS", (x_pos, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    cv2.imshow("pi_cam", frame)

    if cv2.waitKey(1) == ord("q"):
        break
    end_time = time()
    loop_time = end_time - start_time
    fps = .99 * fps + .01 * 1 / loop_time

cv2.destroyAllWindows()