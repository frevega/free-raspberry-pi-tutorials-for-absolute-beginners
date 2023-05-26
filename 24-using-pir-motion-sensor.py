import RPi.GPIO as GPIO
from RepeatTimer import RepeatTimer

GPIO.setmode(GPIO.BOARD)
pirPin = 12
GPIO.setup(pirPin, GPIO.IN)
thread = None

def readSensor():
    print(f"{GPIO.input(pirPin)}      ", end = "\r")

try:
    thread = RepeatTimer(.05, readSensor)
    thread.start()
    
    while True:
        pass
except KeyboardInterrupt:
    thread.cancel()
    GPIO.cleanup()
    print("\nSee ya later, RPi!\n")