import RPi.GPIO as GPIO
from time import sleep

passiveBuzzerPin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(passiveBuzzerPin, GPIO.OUT)
pwm = GPIO.PWM(passiveBuzzerPin, 400)
pwm.start(50)

try:
    while True:
        for i in range(150, 2000):
            pwm.ChangeFrequency(i)
            sleep(.0001)
        for i in range(2000, 150, -1):
            pwm.ChangeFrequency(i)
            sleep(.0001)
except KeyboardInterrupt:
    GPIO.output(passiveBuzzerPin, GPIO.HIGH)
    print(GPIO.input(passiveBuzzerPin))
    GPIO.cleanup()
    print("See you later RPi!")
