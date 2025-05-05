import cv2
from picamera2 import Picamera2
from libcamera import Transform, controls
from time import time, sleep
from threading import Event, Thread

print("Info:", Picamera2.global_camera_info())

# win_length = 1920 # 22-23 @30-60-75-120 Pi5
# win_height = 1080
# win_length = 1280 # 30-31 @30 // 55 @55 // 49-57 @60 // 49-60 @75 // 59-60 @120 Pi5
# win_height = 720
# win_length = 896 # 48 @60 // 111 @120 Pi5
# win_height = 504
# win_length = 854 # 60-63 @60 // 111 @120 Pi5
# win_height = 480
win_length = 640 # 60-63 @60 // 111 @120 Pi5
win_height = 360

def camera(id):
    pi_cam = Picamera2(camera_num = id)
    pi_cam.preview_configuration.main.size = (win_length, win_height)
    
    pi_cam.preview_configuration.main.format = "RGB888"
    pi_cam.preview_configuration.controls.FrameRate = 60 if pi_cam.camera_idx == 0 else 50
    pi_cam.preview_configuration.transform = Transform(hflip = 1)
    pi_cam.preview_configuration.align()
    # pi_cam.configure("preview")
    pi_cam.start()

    if pi_cam.camera_idx == 0:
        pi_cam.set_controls({"AfMode": controls.AfModeEnum.Manual.Continuous})

    return pi_cam

def size_of(frame):
    width = len(frame) -1
    lenght = len(frame[width]) -1

    return frame[width][lenght]

box_side = 100
box_border = -1
box_step = 1
x = 0
y = 0
fps = 0

def cv2_camera(idx):
    global x, y, fps
    pi_cam = camera(idx)
    h_delta = (-1, 1)
    v_delta = (-1, 1)
    x_pos = pi_cam.preview_configuration.main.size[0] - 200
    count_h = 0
    count_v = 0
    while True:
        start_time = time()
        frame = pi_cam.capture_array()
        coord0 = (x, y)
        coord1 = (x + box_side, y + box_side)

        for row in frame:
            for pixel in row:
                if count_v % 72 == 0:
                    pixel[0] = 12
                    pixel[1] = 24
                    pixel[2] = 96
                if count_h % 80 == 0:
                    pixel[0] = 12
                    pixel[1] = 24
                    pixel[2] = 96
                count_h += 1
            count_v += 1
                
        if coord0[0] < 0 or coord1[0] >= win_length - 1 and h_delta[0] != h_delta[1]:
            h_delta = (h_delta[1], h_delta[1] * -1)
        x = x + box_step * h_delta[1]
        if coord0[1] < 0 or coord1[1] >= win_height - 1 and v_delta[0] != v_delta[1]:
            v_delta = (v_delta[1], v_delta[1] * -1)
        y = y + box_step * v_delta[1]

        cv2.rectangle(frame, coord0, coord1, (0, 255, 0), box_border)
        cv2.putText(frame, f"{fps:.0f} FPS", (x_pos, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
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
    for cam_idx in range(1):
        jobs.append(Thread(target = cv2_camera(1), daemon = True))
        jobs[cam_idx].start()

    print("== EXAMPLE COMPLETE ==")

# thread0 = Thread(target = cv2_camera(0), daemon = True)
# thread0.start()

# thread1 = Thread(target = cv2_camera(1), daemon = True)
# thread1.start()