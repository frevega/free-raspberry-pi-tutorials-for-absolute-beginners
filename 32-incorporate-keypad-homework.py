import pigpio
from time import sleep
from RepeatTimer import RepeatTimer

class KeyPad:
    def __init__(self, pi, rows, cols, keys):
        self.pi = pi
        self.rows = rows
        self.cols = cols
        self.keys = keys
        
        [self.pi.set_mode(pin, pigpio.OUTPUT) for pin in rows]
        [self.prepareInputs(pin) for pin in cols]
        
        self.buttonStates = [[[0, 1] for col in cols] for row in rows]
        self.readTimer = None
        self.pressedKeys = []
        
    def prepareInputs(self, pin):
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
        
    def read(self):
        for i, rowPin in enumerate(self.rows):
            self.pi.write(rowPin, 1)
            for j, colPin in enumerate(self.cols):
                self.buttonStates[i][j][0] = self.pi.read(colPin)
                if self.buttonStates[i][j][0] \
                   and self.buttonStates[i][j][0] != self.buttonStates[i][j][1]:
                    self.input(self.keys[i][j])
                self.buttonStates[i][j][1] = self.buttonStates[i][j][0]
            self.pi.write(rowPin, 0)

    def input(self, letter):
        if letter == "D":
            print(" ".join(map(str, self.pressedKeys)))
            self.pressedKeys.clear()
        else:
            self.pressedKeys.append(letter)
            print(" ".join(map(str, ["*" for letter in self.pressedKeys])), end = "\r")
    
    def start(self):
        self.readTimer = RepeatTimer(.1, self.read)
        self.readTimer.start()
    
    def stop(self):
        self.readTimer.cancel()
        self.pi.stop()
        
if __name__ == "__main__":
    try:
        lesson = KeyPad(
            pi = pigpio.pi(),
            rows = [4, 17, 27, 22],
            cols = [5, 19, 20, 21],
            keys = [
                [1, 2, 3, "A"],
                [4, 5, 6, "B"],
                [7, 8, 9, "C"],
                ["*", 0, "#", "D"]
            ]
        )
        lesson.start()
        
        while True:
            sleep(.1)
    except KeyboardInterrupt:
        lesson.stop()
        print("See you later RPi!")
