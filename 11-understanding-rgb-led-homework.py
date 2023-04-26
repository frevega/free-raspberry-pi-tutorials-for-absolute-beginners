import pigpio
from threading import Timer
from time import sleep

class RPiLesson12HW:
    pi = None
    buttonStates: list[list[int]] = [[]]
    ledStates = [0, 0, 0]
    timer = None

    def __init__(self, leds: list[int], buttons: list[int]):
        self.pi = pigpio.pi()
        
        self.leds = [self.prepareLed(n) for n in leds]
        self.buttons = [self.prepareButton(n) for n in buttons]
        self.buttonStates = [[0, 0] for _ in buttons]
 
    def prepareButton(self, pin: int) -> int:
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_UP)
        
        return pin

    def prepareLed(self, pin: int) -> int:
        self.pi.set_mode(pin, pigpio.OUTPUT)
        
        return pin

    def run(self):
        for index, button in enumerate(self.buttons):
            self.buttonStates[index][0] = self.pi.read(button)
            if self.buttonStates[index][0] == 0 and self.buttonStates[index][0] != self.buttonStates[index][1]:
                self.pi.write(self.leds[index], (self.pi.read(self.leds[index]) + 1) % 2)
            self.buttonStates[index][1] = self.buttonStates[index][0]
        self.timer = Timer(.1, self.run)
        self.timer.start()

    def deinit(self):
        _ = [self.pi.write(n, 0) for n in self.leds]
        self.timer.cancel()
        self.pi.stop()

if __name__ == "__main__":
    try:
        homework = RPiLesson12HW(
            leds = [26, 19, 13],
            buttons = [18, 15, 14]
        )
        homework.run()
        
        i = 0
        while True:
            i += 1
            print(i, end = "\r")
            sleep(1)
    except KeyboardInterrupt:
        homework.deinit()
        print("\nSee ya later, RPi Pico!")
