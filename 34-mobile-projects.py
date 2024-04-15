import LCD1602
from KeyPad import KeyPad
from time import sleep

if __name__ == "__main__":
    try:
        masking_key = "_"
        keypad = KeyPad(masking_key = masking_key)
        keypad.start_timer()
        LCD1602.init(0x27)
        LCD1602.clear()

        while True:
            LCD1602.write(0, 0, "Input value:")
            user_input = keypad.read_key_pad()
            if user_input != None:
                LCD1602.write(0, 1, user_input)
                if masking_key not in user_input:
                    LCD1602.write(0, 0, "User input was:")
                    keypad.stop_timer()
                    sleep(3)
                    LCD1602.clear()
                    keypad.start_timer()

    except KeyboardInterrupt:
        sleep(.2)
        LCD1602.clear()
        keypad.stop()
        print("See you later RPi!")