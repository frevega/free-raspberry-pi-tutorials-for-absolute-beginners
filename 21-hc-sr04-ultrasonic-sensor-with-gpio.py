import RPi.GPIO as GPIO
from time import sleep, time

GPIO.setmode(GPIO.BCM)
trigPin = 23
echoPin = 24
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

def echo():
    GPIO.output(trigPin, 0)
    sleep(2E-6) # 1 sec = 1.000.000 microsecs
    GPIO.output(trigPin, 1)
    sleep(10E-6) # 1 sec = 1.000.000 microsecs
    GPIO.output(trigPin, 0)
    
    while GPIO.input(echoPin) == 0:
        pass
    echoStartTime = time()
    while GPIO.input(echoPin) == 1:
        pass
    echoStopTime = time()
    pingTravelTime = echoStopTime - echoStartTime
#     print(pingTravelTime,f"{format(pingTravelTime * 1E6, '.2f')}", end = "\r")
    print(f"{format(1/29.154 * pingTravelTime * 1E6/2, '.2f')} cm          ", end = "\r")
    sleep(.2)

try:
    while True:
        echo()
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Bye!")