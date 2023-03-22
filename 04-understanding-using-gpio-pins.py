import RPi.GPIO as GPIO
from time import sleep

BOARD_PIN_11 = 11
BCM_PIN_17 = 17

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BOARD_PIN_11, GPIO.OUT)

for _ in range(0, 3):
    GPIO.output(BOARD_PIN_11, GPIO.HIGH)
    sleep(.5)
    GPIO.output(BOARD_PIN_11, GPIO.LOW)
    sleep(.5)

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(BCM_PIN_17, GPIO.OUT)

for _ in range(0, 5):
    GPIO.output(BCM_PIN_17, GPIO.HIGH)
    sleep(.1)
    GPIO.output(BCM_PIN_17, GPIO.LOW)
    sleep(.1)

GPIO.cleanup()