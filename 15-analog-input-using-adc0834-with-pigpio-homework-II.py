import pigpio
import ADC0834
from threading import Timer
from time import sleep

ADC0834.setup()
pi = pigpio.pi()
ledPin = 26
pi.set_PWM_dutycycle(ledPin, 0)
pi.set_PWM_frequency(ledPin, 1000)
adcResult = 0
timer = None

def main():
    global timer, adcResult
    adcResult = ADC0834.getResult()
    pi.set_PWM_dutycycle(ledPin, adcResult)
    print(f"{adcResult:03}", end = "\r")
    timer = Timer(.1, main)
    timer.start()

try:
    main()
#     while True:
#         print(f"{ADC0834.getResult():03}", end = "\r")
#         sleep(.1)

except (KeyboardInterrupt, RuntimeError) as error:
    timer.cancel()
    pi.stop()
    print("\nSee ya later, RPi!\n", error)