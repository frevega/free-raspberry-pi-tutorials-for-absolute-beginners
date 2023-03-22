import RPi.GPIO as GPIO
# from time import sleep

ledPin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
# GPIO.output(ledPin, GPIO.HIGH) # Digital ON

# print("Duty cycle: 255")
pwmPin = GPIO.PWM(ledPin, 100) # pin, freq
pwmPin.start(100) # duty cycle
sleep(5)

print("Duty cycle: 100")
pwmPin.ChangeDutyCycle(100)
sleep(5)

print("Frequency: 75")
pwmPin.ChangeFrequency(75)
sleep(5)

print("Frequency: 30")
pwmPin.ChangeFrequency(30)
sleep(5)

print("Duty cycle: 0")
pwmPin.stop(10)
GPIO.cleanup()



import RPi.GPIO as GPIO
from time import sleep
ledPin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
pwmPin = GPIO.PWM(ledPin, 60)
pwmPin.start(50)
sleep(10)
pwmPin.stop()
GPIO.cleanup()