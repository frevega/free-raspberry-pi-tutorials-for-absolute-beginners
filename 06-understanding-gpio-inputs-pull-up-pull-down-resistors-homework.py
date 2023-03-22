import RPi.GPIO as GPIO
from time import sleep

ledPin = 38
buttonPin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)

try:
    while True:
        GPIO.output(ledPin, GPIO.input(buttonPin))
        print(GPIO.input(buttonPin))
        sleep(.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("See ya later!")