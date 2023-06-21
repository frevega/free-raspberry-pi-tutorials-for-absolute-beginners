import pigpio
from RepeatTimer import RepeatTimer

pi = pigpio.pi()
pirPin = 12
pi.set_mode(pirPin, pigpio.INPUT)

thread = None

def readSensor():
    print(f"{pi.read(pirPin)}      ", end = "\r")

try:
    thread = RepeatTimer(.05, readSensor)
    thread.start()
    
    while True:
        pass
except KeyboardInterrupt:
    thread.cancel()
    pi.stop()
    print("\nSee ya later, RPi!\n")