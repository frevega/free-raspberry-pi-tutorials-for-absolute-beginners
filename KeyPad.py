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
            enter_key = "D",
            masking_key = "_",
            is_debugging = False
        ):
        if len([masking_key for list in keys if masking_key in list]) > 0:
            raise IOError(f"Masking key '{masking_key}' should not exist in keys list")
        else:
            self.pi = pi
            self.rows = rows
            self.cols = cols
            self.keys = keys
            self.enter_key = enter_key
            self.masking_key = masking_key
            
            [self.pi.set_mode(pin, pigpio.OUTPUT) for pin in rows]
            [self.prepare_inputs(pin) for pin in cols]
            
            self.button_states = [[[0, 1] for col in cols] for row in rows]
            self.read_timer = None
            self.pressed_keys = []
            """ Keeps latest keystroke """
            self.pressed_key = ""
            self.is_debugging = is_debugging
        
    def prepare_inputs(self, pin):
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
        
    def read(self):
        for i, row_pin in enumerate(self.rows):
            self.pi.write(row_pin, 1)
            for j, col_pin in enumerate(self.cols):
                self.button_states[i][j][0] = self.pi.read(col_pin)
                if self.button_states[i][j][0] \
                   and self.button_states[i][j][0] != self.button_states[i][j][1]:
                    self.pressed_key = self.keys[i][j]
                    self.check_input()
                self.button_states[i][j][1] = self.button_states[i][j][0]
            self.pi.write(row_pin, 0)
    
    def check_input(self):
        """ Check if mapped key was pressed in order to return string """
        if self.pressed_key == self.enter_key:
            self.aux_input = " ".join(map(str, self.pressed_keys))
            if self.is_debugging:
                print(self.aux_input)
            self.pressed_keys.clear()
        else:
            self.pressed_keys.append(self.pressed_key)
            if self.is_debugging:
                print(" ".join(map(str, [self.masking_key for letter in self.pressed_keys])), end = "\r")

    def read_key_pad(self):
        if self.pressed_key == self.enter_key and len(self.aux_input) != 0:
            self.pressed_key = ""
            return self.aux_input.replace(" ", "")
        elif len(self.pressed_keys) != 0:
            return "".join(map(str, [self.masking_key for letter in self.pressed_keys]))
        
        return None
    
    def start_timer(self):
        self.read_timer = RepeatTimer(.1, self.read)
        self.read_timer.start()

    def stop_timer(self):
        if self.read_timer != None:
            self.read_timer.cancel()
            self.read_timer = None
    
    def stop(self):
        self.stop_timer()
        self.pi.stop()
