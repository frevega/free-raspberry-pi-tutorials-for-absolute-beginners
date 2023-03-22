import pigpio
# from time import sleep

ledPin = 19
pi = pigpio.pi()
# Not needed according to
# https://forums.raspberrypi.com/viewtopic.php?t=244692
# pi.set_mode(ledPin, pigpio.OUTPUT)

def ledPWM(start: int, stop: int, step: int, pause: float):
    for value in range(start, stop, step):
        pi.set_PWM_dutycycle(ledPin, value)
        sleep(pause)

#ledPWM(0, 255, 5, .01)
#ledPWM(254, -1, -1, .01)

print("Duty cycle: 255")
pi.set_PWM_dutycycle(ledPin, 255)
sleep(5)

print("Duty cycle: 100")
pi.set_PWM_dutycycle(ledPin, 100)
sleep(5)

print("Frequency: 75")
pi.set_PWM_frequency(ledPin, 75)
sleep(5)

print("Frequency: 30")
pi.set_PWM_frequency(ledPin, 30)
sleep(5)

print("Duty cycle: 0")
pi.set_PWM_dutycycle(ledPin, 0)
pi.stop()





import pigpio
from time import sleep
ledPin = 19
pi = pigpio.pi()
pi.set_PWM_dutycycle(ledPin, 122.5)
pi.set_PWM_frequency(ledPin, 60)
sleep(10)
pi.set_PWM_dutycycle(ledPin, 0)
pi.set_PWM_frequency(ledPin, 0)
pi.stop()