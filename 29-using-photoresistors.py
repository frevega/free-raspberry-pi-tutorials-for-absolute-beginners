import pigpio
import ADC0834
from time import sleep

pi = pigpio.pi()
ADC0834.setup()

try:
    while True:
        print(f"Light value: {ADC0834.getResult()}  ", end = "\r")
        sleep(.1)
except KeyboardInterrupt:
    pi.stop()
    print("See you later RPi!")