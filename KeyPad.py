import pigpio
from RepeatTimer import RepeatTimer

class KeyPad:
    def __init__(
            self, 
            pi = pigpio.pi(), 
            rows = [4, 17, 27, 22], 
            cols = [5, 6, 13, 19], 
            keys = [
                [1, 2, 3, "A"],
                [4, 5, 6, "B"],
                [7, 8, 9, "C"],
                ["*", 0, "#", "D"]
            ],
            enterKey = "D"
        ):
        self.pi = pi
        self.rows = rows
        self.cols = cols
        self.keys = keys
        self.enterKey = enterKey
        
        [self.pi.set_mode(pin, pigpio.OUTPUT) for pin in rows]
        [self.prepareInputs(pin) for pin in cols]
        
        self.buttonStates = [[[0, 1] for col in cols] for row in rows]
        self.readTimer = None
        self.pressedKeys = []
        """ Keeps latest keystroke """
        self.pressedKey = ""
        
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
                    self.pressedKey = self.keys[i][j]
                    self.check_input()
                self.buttonStates[i][j][1] = self.buttonStates[i][j][0]
            self.pi.write(rowPin, 0)
    
    def check_input(self):
        """ Check if mapped key was pressed in order to return string """
        if self.pressedKey == self.enterKey:
            self.auxInputString = " ".join(map(str, self.pressedKeys))
            print(self.auxInputString)
            self.pressedKeys.clear()
        else:
            self.pressedKeys.append(self.pressedKey)
            print(" ".join(map(str, ["*" for letter in self.pressedKeys])), end = "\r")

    def readKeyPad(self):
        if self.pressedKey == self.enterKey and len(self.auxInputString) != 0:
            self.pressedKey = ""
            
            return self.auxInputString.replace(" ", "")
        
        return None
    
    def startTimer(self):
        self.readTimer = RepeatTimer(.1, self.read)
        self.readTimer.start()

    def stopTimer(self):
        if self.readTimer != None:
            self.readTimer.cancel()
            self.readTimer = None
    
    def stop(self):
        self.stopTimer()
        self.pi.stop()
