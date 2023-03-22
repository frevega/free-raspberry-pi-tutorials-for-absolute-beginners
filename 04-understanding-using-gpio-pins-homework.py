import RPi.GPIO as GPIO
from time import sleep

def blinky():
    exit = False
    BOARD_PIN_11 = 11

    while not exit:
        blinkTimes = input("How many times would you wanna blink the led? ")
        if not blinkTimes.isnumeric() or int(blinkTimes) <= 0:
            print("Only positive numbers please!")
            continue
        else:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(BOARD_PIN_11, GPIO.OUT)

            for blink in range(1, int(blinkTimes) + 1):
                print(blink)
                GPIO.output(BOARD_PIN_11, GPIO.HIGH)
                sleep(.25)
                GPIO.output(BOARD_PIN_11, GPIO.LOW)
                sleep(.25)

            GPIO.cleanup()
            print(F"Done, led blinked {blinkTimes} times!")
            exit = blink_again()

def blink_again():
    while True:
        shouldGoAgain = input("Should we go again (y/n)? ")
        if shouldGoAgain.lower() in ("y", "n"):
            if shouldGoAgain.lower() == "y":
                print()
                return False
            else:
                print("See ya next time!")
                return True
        else:
            continue

blinky()
