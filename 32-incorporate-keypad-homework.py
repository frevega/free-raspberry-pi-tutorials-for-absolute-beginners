from KeyPad import KeyPad
from time import sleep

if __name__ == "__main__":
    try:
        lesson = KeyPad()
        lesson.start()
        
        while True:
            sleep(.1)
    except KeyboardInterrupt:
        lesson.stop()
        print("See you later RPi!")
