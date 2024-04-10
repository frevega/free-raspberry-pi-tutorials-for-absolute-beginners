from time import sleep
from threading import Thread

def myBox(delay):
    while True:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Box open")
        sleep(delay)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Box closed")
        sleep(delay)

def myLED(delay):
    while True:
        print("LED on")
        sleep(delay)
        print("LED off")
        sleep(delay)

boxThread = Thread(target = myBox, args = (5,), daemon = True)
LEDThread = Thread(target = myLED, args = (1,), daemon = True)

boxThread.start()
LEDThread.start()

j = 0
while True:
    j += 1
    print(j)
    sleep(.1)
