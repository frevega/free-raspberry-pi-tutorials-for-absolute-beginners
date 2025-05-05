import cv2
from picamera2 import Picamera2
from libcamera import controls
from time import time
from threading import Thread

print("Info:", Picamera2.global_camera_info())

def camera(id):
    pi_cam = Picamera2(camera_num = id)
    # pi_cam.preview_configuration.main.size = (1920, 1080) # 22-23 @30-60-75-120 Pi5
    # pi_cam.preview_configuration.main.size = (1280, 720) # 30-31 @30 // 55 @55 // 49-57 @60 // 49-60 @75 // 59-60 @120 Pi5
    # pi_cam.preview_configuraqtion.main.size = (896, 504) # 48 @60 // 111 @120 Pi5
    # pi_cam.preview_configuration.main.size = (854, 480) # 60 @60 // 111 @120 Pi5
    pi_cam.preview_configuration.main.size = (640, 360) # 60-63 @60 // 111 @120 Pi5

    pi_cam.preview_configuration.main.format = "RGB888"
    pi_cam.preview_configuration.controls.FrameRate = 60 if pi_cam.camera_idx == 0 else 50
    # pi_cam.preview_configuration.transform = Transform(vflip = 1)
    pi_cam.preview_configuration.align()
    # pi_cam.configure("preview")
    pi_cam.start()

    if pi_cam.camera_idx == 0:
        pi_cam.set_controls({"AfMode": controls.AfModeEnum.Manual.Continuous})

    return pi_cam

fps = 0

# x_pos = pi_cameras[0].preview_configuration.main.size[0] - 200

def size_of(frame):
    width = len(frame) -1
    lenght = len(frame[width]) -1

    return frame[width][lenght]

# for pi_cam in pi_cameras:
def cv2_camera(idx):
    global fps
    pi_cam = camera(idx)
    x_pos = pi_cam.preview_configuration.main.size[0] - 200
    while True:
        start_time = time()
        frame = pi_cam.capture_array()
        cv2.putText(frame, f"{fps:.0f} FPS", (x_pos, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        cv2.putText(frame, f"{size_of(frame)}", (x_pos -200, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.rectangle(frame, (50, 50), (200, 150), (0, 255, 0), -1)
        cv2.circle(frame, (480, 200), 50, (255, 0, 0), 2)
        cv2.imshow(f"pi_cam{pi_cam.camera_idx}", frame)

        if cv2.waitKey(1) == ord("q"):
            break
        end_time = time()
        loop_time = end_time - start_time
        fps = .99 * fps + .01 * 1 / loop_time

    cv2.destroyAllWindows()

def cv2_camera2(idx):
    print(idx)

if __name__ == "__main__":
    jobs = []
    for cam_idx in range(2):
        jobs.append(Thread(target = cv2_camera(cam_idx), daemon = True))
        jobs[cam_idx].start()

    print("== EXAMPLE COMPLETE ==")

# thread0 = Thread(target = cv2_camera(0), daemon = True)
# thread0.start()

# thread1 = Thread(target = cv2_camera(1), daemon = True)
# thread1.start()