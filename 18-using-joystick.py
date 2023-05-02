import ADC0834
import RPi.GPIO as GPIO
from RepeatTimer import RepeatTimer
from time import sleep

GPIO.setmode(GPIO.BCM)

buttonPin = 21
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

ADC0834.setup()
adcResults = [0, 0]
timer = None

def main():
    global adcResults
    for index, pot in enumerate(adcResults):
        adcResults[index] = ADC0834.getResult(index)

try:
    timer = RepeatTimer(.01, main)
    timer.start()
    while True:
        print(f"X: {adcResults[0]:03} Y: {adcResults[1]:03} B: {GPIO.input(buttonPin)}", end = "\r")
        sleep(.1)
except KeyboardInterrupt:
    timer.cancel()
    GPIO.cleanup()
    print("\nSee ya later, RPi!\n")

