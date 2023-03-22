import RPi.GPIO as GPIO
from time import sleep

ledPin = 38
buttonPin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    while True:
        GPIO.output(ledPin, GPIO.LOW if GPIO.input(buttonPin) is GPIO.HIGH else GPIO.HIGH)
        print(GPIO.input(buttonPin))
        sleep(.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("See ya later!")
