import RPi.GPIO as GPIO
from time import sleep

ledState = GPIO.LOW
buttonPrevState = GPIO.HIGH

ledPin = 38
buttonPin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(buttonPin) == GPIO.HIGH and GPIO.input(buttonPin) != buttonPrevState:
            ledState = (ledState + 1) % 2
            print("Led on" if ledState == GPIO.HIGH else "Led off")
        buttonPrevState = GPIO.input(buttonPin)
        GPIO.output(ledPin, ledState)
        sleep(.1)

except KeyboardInterrupt:
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.cleanup()
    print("See ya later!")
    