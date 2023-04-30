# p1 (x1 = 0, y1 = 0)
# p2 (x2 = 255, y2 = 100)
#
# Slope m = y2 - y1   100 - 0   100
#           ------- = ------- = ---
#           x2 - x1   255 - 0   255
#
# Equation of the line
#
# y - y1 = m (x - x1) = y - 0 = 100 (x - 0) = y = 100 . x
#                               ---               ---
#                               255               255

import RPi.GPIO as GPIO
import ADC0834
from threading import Timer
from time import sleep

ADC0834.setup()
GPIO.setmode(GPIO.BCM)
ledPin = 21
GPIO.setup(ledPin, GPIO.OUT)
pwmPin = GPIO.PWM(ledPin, 1000) # pin, freq
pwmPin.start(0) # duty cycle
newDuty = 0
timer = None

def main():
    newDuty = (100/255) * ADC0834.getResult()
    pwmPin.ChangeDutyCycle(newDuty)
    timer = Timer(.1, main)
    timer.start()

try:
    main()
    while True:
        print(f"{ADC0834.getResult():03}", end = "\r")# - {newDuty:03}", end = "\r")
        sleep(.1)

except KeyboardInterrupt:
    timer.cancel()
    pwmPin.stop()
    GPIO.cleanup()
    print("\nSee ya later, RPi!")
