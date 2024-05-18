from time import sleep
from threading import Event, Thread

def myBox(delay, event):
    while True:
        print(">>>>>>>>>> Box open")
        sleep(delay)
        print("<<<<<<<<<< Box closed")
        sleep(delay)
        if event.is_set():
            break
    print("========== myBox worker closing down")

def myLED(delay):
    while True:
        print("LED on")
        sleep(delay)
        print("LED off")
        sleep(delay)

event = Event()
boxThread = Thread(target = myBox, args = (3, event), daemon = True)
LEDThread = Thread(target = myLED, args = (1,), daemon = True)

boxThread.start()
LEDThread.start()

j = 0
while True:
    j += 1
    print(j)
    sleep(.1)
    if j == 100:
        print("Stopping thread?")
        event.set()
        # boxThread.join()
    if j == 150:
        print("Continuing thread?")
        boxThread.start() # RuntimeError: threads can only be started once