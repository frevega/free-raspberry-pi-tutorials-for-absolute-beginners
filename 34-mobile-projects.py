import LCD1602
from KeyPad import KeyPad
from time import sleep

if __name__ == "__main__":
    try:
        keypad = KeyPad()
        keypad.startTimer()

        LCD1602.init(0x27)
        
        while True:
            LCD1602.write(0, 0, "Input value:")
            userInput = keypad.readKeyPad()
            
            if userInput != None:
                LCD1602.write(0, 0, "User input was:")
                LCD1602.write(0, 1, userInput)
                keypad.stopTimer()
                sleep(3)
                LCD1602.clear()
                keypad.startTimer()
    except KeyboardInterrupt:
        sleep(.2)
        LCD1602.clear()
        keypad.stop()
        print("See you later RPi!")