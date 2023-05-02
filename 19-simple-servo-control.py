# PWM period 20 ms = 0.02 seconds
# RPi takes frequency (hertz) instead of period
#
#           1        1
# freq =  ------ = ---- = 50Hz
#         period   0.02
#
# Duty cycle
# DC ≈ 1 -> 2% -> 0
# DC ≈ 10 -> 15% -> 180

import pigpio
from RepeatTimer import RepeatTimer
from time import sleep

servoPin = 26
pi = pigpio.pi()
pi.set_mode(servoPin, pigpio.OUTPUT)
pi.set_PWM_frequency(servoPin, 50)
pi.set_PWM_range(servoPin, 10000)
angle = 0

def set_angle(new_angle):
    global angle
    if new_angle > 90:
        new_angle = 90
    elif new_angle < -90:
        new_angle = -90
    angle = new_angle
    duty = map(angle, -90, 90, 1250, 250)
    pi.set_PWM_dutycycle(servoPin, duty)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def smooth_pos(newPos):
    global angle
    for r in range(angle, newPos, (1 if newPos > angle else -1)):
        set_angle(r)
        sleep(.01)

try:
    set_angle(0)
    while True:
        smooth_pos(int(input("PWM % (90 ~ -90): ")))
except KeyboardInterrupt:
    pi.stop()
    print("\nSee ya later, RPi!\n")