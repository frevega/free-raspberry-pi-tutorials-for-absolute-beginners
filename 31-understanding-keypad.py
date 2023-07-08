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
        
        self.readTimer = None
        self.writeTimer = None
        self.pressedKeys = []
        
    def prepareInputs(self, pin):
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
        
    def read(self):
        for i, row in enumerate(self.rows):
            self.pi.write(row, 1)
            for j, col in enumerate(self.cols):
                if self.pi.read(col) == 1:
                    self.pressedKeys.append(self.keys[i][j])
                    sleep(.25)
            self.pi.write(row, 0)
    
    def write(self):
        print(self.pressedKeys, end = "\r")
    
    def start(self):
        self.readTimer = RepeatTimer(.1, self.read)
        self.readTimer.start()
        self.writeTimer = RepeatTimer(.1, self.write)
        self.writeTimer.start()
    
    def stop(self):
        self.readTimer.cancel()
        self.writeTimer.cancel()
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