import RPi.GPIO as GPIO
from RepeatTimer import RepeatTimer

GPIO.setmode(GPIO.BOARD)
pirPin = 12
ledPin = 16
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
thread = None

def readSensor():
    output = GPIO.input(pirPin)
    print(f"{output}      ", end = "\r")
    toggleLed(output)
    
def toggleLed(value):
    GPIO.output(ledPin, value)

try:
    thread = RepeatTimer(.05, readSensor)
    thread.start()
    
    while True:
        pass
except KeyboardInterrupt:
    thread.cancel()
    GPIO.cleanup()
    print("\nSee ya later, RPi!\n")
