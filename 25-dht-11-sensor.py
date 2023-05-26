import RPi.GPIO as GPIO
from dht11 import DHT11
from time import sleep

class Lesson24:
    def __init__(self, boardMode: int, dhtPin: int):
        GPIO.setmode(boardMode)
        self.dht = DHT11(pin = dhtPin)
        
    def getRead(self):
        read = self.dht.read()
        if read.is_valid():
            print(f"T: {read.temperature}, H: {read.humidity}     ", end = "\r")
        sleep(.2)

    def cleanup(self):
        GPIO.cleanup()
        print("\nSee you later RPi!")

if __name__ == "__main__":
    try:
        lesson = Lesson24(boardMode = GPIO.BCM, dhtPin = 17)
        while True:
            lesson.getRead()
    except KeyboardInterrupt:
        lesson.cleanup()