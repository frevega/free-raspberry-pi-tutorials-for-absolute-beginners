import pigpio as GPIO
from time import sleep

MAX_DUTY = 255.0
DUTY_STEPS = 8

ledValue = 0 # 255.0
buttonIncPrevState = 1
buttonDecPrevState = 1

ledPin = 19
buttonIncPin = 21
buttonDecPin = 26

pi = GPIO.pi()
pi.set_mode(buttonIncPin, GPIO.INPUT)
pi.set_mode(buttonDecPin, GPIO.INPUT)
pi.set_pull_up_down(buttonIncPin, GPIO.PUD_UP)
pi.set_pull_up_down(buttonDecPin, GPIO.PUD_UP)
pi.set_PWM_dutycycle(ledPin, 0)
pi.set_PWM_frequency(ledPin, 60)

# Third attempt, logarithmic
buttonPushes = 0
magicNumber = 1.74042

try:
    while True:
        if pi.read(buttonIncPin) == 1 and pi.read(buttonIncPin) != buttonIncPrevState and ledValue < MAX_DUTY:
            # First attempt, arithmetic progression
#             ledValue = MAX_DUTY if ledValue + (MAX_DUTY / DUTY_STEPS) > MAX_DUTY else ledValue + (MAX_DUTY / DUTY_STEPS)
            # Scond attempt, geometric progression
#             ledValue = ledValue * 2
            # Third attempt, logarithmic progression
            buttonPushes += 1
            ledValue = magicNumber ** buttonPushes
            print(f"Duty cycle incremented {format(ledValue, '.2f')}")
        elif pi.read(buttonDecPin) == 1 and pi.read(buttonDecPin) != buttonDecPrevState and ledValue >= magicNumber:
            # First attempt, arithmetic progression
#             ledValue = 0 if ledValue - (MAX_DUTY / DUTY_STEPS) < 0 else ledValue - (MAX_DUTY / DUTY_STEPS)
            # Scond attempt, geometric progression
#             ledValue = ledValue / 2
            # Third attempt, logarithmic progression
            buttonPushes -= 1
            ledValue = 0 if magicNumber ** buttonPushes < magicNumber else magicNumber ** buttonPushes
            print(f"Duty cycle decremented {format(ledValue, '.2f')}")
        buttonIncPrevState = pi.read(buttonIncPin)
        buttonDecPrevState = pi.read(buttonDecPin)
        pi.set_PWM_dutycycle(ledPin, ledValue)
        sleep(.1)

except KeyboardInterrupt:
    pi.write(ledPin, 0)
    pi.stop()
    print("See ya later!")
    
