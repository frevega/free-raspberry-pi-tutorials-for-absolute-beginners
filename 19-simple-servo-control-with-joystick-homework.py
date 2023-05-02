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

import RPi.GPIO as GPIO
import ADC0834
import pigpio
from threading import Thread
from time import sleep

GPIO.setmode(GPIO.BCM)
ADC0834.setup()
servoPin = 26
pi = pigpio.pi()
pi.set_mode(servoPin, pigpio.OUTPUT)
pi.set_PWM_frequency(servoPin, 50)
pi.set_PWM_range(servoPin, 10000)
angle = 0
adcResult = 0

isPosLocked = False
buttonStates = [0, 0]

buttonPin = 21
pi.set_mode(buttonPin, pigpio.INPUT)
pi.set_pull_up_down(buttonPin, pigpio.PUD_UP)

def set_angle(new_angle):
    global angle
    if new_angle > 255:
        new_angle = 255
    elif new_angle < 0:
        new_angle = 0
    angle = new_angle
    duty = map(angle, 0, 255, 1250, 250)
    pi.set_PWM_dutycycle(servoPin, duty)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def smooth_pos(newPos):
    global angle
    for r in range(angle, newPos, (1 if newPos > angle else -1)):
        set_angle(r)
        sleep(.005)

def lockPos() -> bool:
    global isPosLocked, buttonStates
    buttonStates[0] = pi.read(buttonPin)
    if buttonStates[0] == 0 and buttonStates[0] != buttonStates[1]:
        isPosLocked = not isPosLocked
    buttonStates[1] = buttonStates[0]
    
    return isPosLocked

def main():
    global adcResult, isPosLocked
    if not lockPos():
        adcResult = ADC0834.getResult(0)
    print(f"X: {adcResult:03} B: {buttonStates[0]} - {isPosLocked}", end = "\r")
    smooth_pos(adcResult)

try:
    set_angle(int(255/2))
    while True:
        main()
except KeyboardInterrupt:
    pi.stop()
    print("\nSee ya later, RPi!\n")
