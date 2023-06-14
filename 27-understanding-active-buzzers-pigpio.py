import pigpio
from time import sleep

activeBuzzerPin = 22
pi = pigpio.pi()
pi.set_mode(activeBuzzerPin, pigpio.OUTPUT)

try:
    while True:
        pi.write(activeBuzzerPin, not pi.read(activeBuzzerPin))
        print(pi.read(activeBuzzerPin))
        sleep(.1)
except KeyboardInterrupt:
    pi.write(activeBuzzerPin, 1)
    print(pi.read(activeBuzzerPin))
    pi.stop()
    print("See you later RPi!")