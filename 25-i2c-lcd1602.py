import LCD1602
from time import sleep

class Lesson25:
    def __init__(self, lcdAddress: int):
        LCD1602.init(lcdAddress)
        
    def write(self, row: int, column: int, message: str):
        LCD1602.write(row, column, message)

    def cleanup(self):
        sleep(.2)
        LCD1602.clear()
        print("\nSee you later RPi!")

if __name__ == "__main__":
    try:
        lesson = Lesson25(lcdAddress = 0x27)
        i = 0
        lesson.write(0, 0, "Hola Mundo!")
        while True:
            i += 1
            lesson.write(0, 1, f"{i}")
            sleep(1)
    except KeyboardInterrupt:
        lesson.cleanup()