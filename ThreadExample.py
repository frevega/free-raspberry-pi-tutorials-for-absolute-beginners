from time import sleep
from threading import Event, Thread

def myBox(delay, event):
    print("======================================== myBox worker starting up")
    while True:
        print(">>>>>>>>>> Box open")
        sleep(delay)
        print("<<<<<<<<<< Box closed")
        sleep(delay)
        if event.is_set():
            break
    print("======================================== myBox worker closing down")

def myLED(delay):
    while True:
        print("LED on")
        sleep(delay)
        print("LED off")
        sleep(delay)

def start_box_thread(delay, event):
    boxThread = Thread(target = myBox, args = (delay, event), daemon = True)
    boxThread.start()

event = Event()
start_box_thread(3, event)
LEDThread = Thread(target = myLED, args = (1,), daemon = True)

LEDThread.start()

j = 0
while True:
    j += 1
    print(j)
    sleep(.1)
    if j % 20 == 0:
        print("Stopping thread?")
        event.set()
        # boxThread.join()
    if j % 50 == 0:
        print("Continuing thread?")
        start_box_thread(15, event) # RuntimeError: threads can only be started once
        event.clear()