import RPi.GPIO as GPIO
import ADC0834
from time import sleep

GPIO.setmode(GPIO.BCM)
ADC0834.setup()

try:
    while True:
        print(ADC0834.getResult())
        sleep(.2)
except KeyboardInterrupt:
    print("\nSee ya later, RPi!")