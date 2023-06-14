import RPi.GPIO as GPIO
from time import sleep

activeBuzzerPin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(activeBuzzerPin, GPIO.OUT)

try:
    while True:
        GPIO.output(activeBuzzerPin, not GPIO.input(activeBuzzerPin))
        print(GPIO.input(activeBuzzerPin))
        sleep(.1)
except KeyboardInterrupt:
    GPIO.output(activeBuzzerPin, GPIO.HIGH)
    print(GPIO.input(activeBuzzerPin))
    GPIO.cleanup()
    print("See you later RPi!")
