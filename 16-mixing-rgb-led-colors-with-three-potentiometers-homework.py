import pigpio
import ADC0834
from threading import Timer

def preparePWMLed(pin: int) -> int:
    pi.set_PWM_dutycycle(pin, 0)
    pi.set_PWM_frequency(pin, 1000)
    
    return pin

ADC0834.setup()
pi = pigpio.pi()
leds = [preparePWMLed(n) for n in [16, 20, 21]]
adcResults = [0 for led in leds]
timer = None

def main():
    global timer, adcResults
    for index, led in enumerate(leds):
        adcResults[index] = ADC0834.getResult(index)
        pi.set_PWM_dutycycle(led, adcResults[index])
    print(f"R: {adcResults[0]:03} G: {adcResults[1]:03} B: {adcResults[2]:03} ", end = "\r")
    timer = Timer(.01, main)
    timer.start()

try:
    main()
    while True:
        pass
except KeyboardInterrupt:
    timer.cancel()
    pi.stop()
    print("\nSee ya later, RPi!\n")
