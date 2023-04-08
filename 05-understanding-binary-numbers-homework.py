import RPi.GPIO as GPIO
from time import sleep

pins = [11, 13, 15, 29, 31]
GPIO.setmode(GPIO.BOARD)
MAX_ITERATION = 32

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
try:
    for iteration in range(MAX_ITERATION):
        for index, pin in enumerate(pins):
            print(f"{iteration} / int(2 ** {index}) % 2 = {int(iteration / 2 ** index) % 2}", end = "\n\n" if index == len(pins) -1 else "\n")
            GPIO.output(pin, int(iteration / 2 ** index) % 2)
        sleep(.25)
    GPIO.cleanup()
except KeyboardInterrupt:
    [GPIO.output(pin, GPIO.LOW) for pin in pins]
    GPIO.cleanup()