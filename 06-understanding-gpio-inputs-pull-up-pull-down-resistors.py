import RPi.GPIO as GPIO
from time import sleep

buttonPin = 40;
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN)

try:
    while True:
        print(GPIO.input(buttonPin))
        sleep(.25)

except KeyboardInterrupt:
    GPIO.cleanup()