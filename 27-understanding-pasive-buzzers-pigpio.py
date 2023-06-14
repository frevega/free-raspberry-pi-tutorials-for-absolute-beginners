import pigpio
from time import sleep

def preparePWM(pin: int) -> int:
    pi.set_PWM_dutycycle(pin, 50)
    pi.set_PWM_frequency(pin, 400)
    
    return pin

passiveBuzzerPin = 22
pi = pigpio.pi()
preparePWM(passiveBuzzerPin)

def test(freq, sleepTime):
    pi.set_PWM_frequency(passiveBuzzerPin, freq)
    sleep(sleepTime)

try:
    while True:
#         [test(freq, 1) for freq in [600, 900]]
        for i in range(150, 2000):
            test(i, .0001)
        for i in range(2000, 150, -1):
            test(i, .0001)
except KeyboardInterrupt:
    pi.write(passiveBuzzerPin, 0)
    print(pi.read(passiveBuzzerPin))
    pi.stop()
    print("See you later RPi!")