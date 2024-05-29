# 1 armed       A
# 2 unarmed     B
# 3 password    C

import LCD1602 as lcd
import pigpio
from enum import Enum
from KeyPad import KeyPad
from RepeatTimer import RepeatTimer
from threading import Event, Thread
from time import sleep

SystemState = Enum("SystemState", ["ARM", "ARMED", "UNARM", "UNARMED", "PASSWORD", "UPDATE_PASSWORD"])

PREVIOUS = 0
CURRENT = 1
PASSW_MAX_TRIES = 3
SECURITY_CHECK_MAX_TRIES = 1

class MySecuritySystem:
    def __init__(self):
        self.__user_input = None
        self.__upd_passw_counter = 0
        self.__lcd_text_to_write = [None, None]
        self.__pi = pigpio.pi()
        self.__prepare_lcd()
        self.__prepare_keypad()
        self.__prepare_motion_sensor()
        self.__stop_motion_sensor_event = Event()
        self.__system_states = [None, SystemState.PASSWORD]
        self.__current_password = [False, None]
        self.__previous_password = [False, None]
        self.__handle_state(SystemState.PASSWORD)
        self.__start_keypad_thread()

    def __prepare_lcd(self):
        lcd.init()
        lcd.clear()
        self.__prepare_lcd_led(100, 200)
    
    def __prepare_lcd_led(self, duty, freq):
        self.__pi.set_PWM_dutycycle(18, duty)
        self.__pi.set_PWM_frequency(18, freq)

    def __prepare_keypad(self):
        self.__keypad = KeyPad(pi = self.__pi)
        self.__keypad.start_timer()

    def __prepare_motion_sensor(self):
        self.__motion_sensor_pin = 23
        self.__pi.set_mode(self.__motion_sensor_pin, pigpio.INPUT)

    def __start_keypad_thread(self):
        self.__read_keypad_action_thread = Thread(target = self.__read_keypad_action, daemon = True)
        self.__read_keypad_action_thread.start()

    def __start_motion_sensor_thread(self):
        self.__stop_motion_sensor_event.clear()
        motion_sensor_thread = Thread(target = self.__read_motion_sensor, args = (self.__stop_motion_sensor_event,), daemon = True)
        motion_sensor_thread.start()

    def __read_motion_sensor(self, event):
        while True:
            print(f"{self.__pi.read(self.__motion_sensor_pin)}", end = "\n")
            sleep(.1)
            if event.is_set():
                break

    def __clear_lcd_row(self, col = 0, row = 1):
        lcd.write(col, row, "".join([" " for space in range(16)]))

    def __write_lcd_text(self, text):
        self.__lcd_text_to_write[0] = self.__lcd_text_to_write[1]
        self.__lcd_text_to_write[1] = text

        if self.__lcd_text_to_write[0] != self.__lcd_text_to_write[1]:
            lcd.write(0, 0, self.__lcd_text_to_write[1])

    def __security_check(self, text, state):
        self.__write_lcd_text(text)
        if self.__user_input in ["A", "B", "C"]:
            self.__user_input = None
            self.__clear_lcd_row()
        elif self.__user_input != None:
            if "_" not in self.__user_input:
                if self.__current_password[1] == self.__user_input:
                    self.__upd_passw_counter = 0
                    self.__handle_state(state)
                else:
                    lcd.write(0, 1, "NO MATCH        ")
                    sleep(1)
                    self.__upd_passw_counter += 1
                    if self.__upd_passw_counter == SECURITY_CHECK_MAX_TRIES:
                        lcd.write(0, 1, "SYSTEM RESET    ")
                        sleep(1)
                        self.__upd_passw_counter = 0
                        self.__handle_state(self.__system_states[PREVIOUS])
                    self.__clear_lcd_row()
            else:
                lcd.write(0, 1, "".join(map(str, ["*" for letter in self.__user_input])))

    def __handle_state(self, state):
        states_check = [SystemState.PASSWORD, SystemState.UPDATE_PASSWORD, SystemState.ARM, SystemState.UNARM]
        if state in states_check and self.__system_states[1] == SystemState.UNARM:
            state = SystemState.UNARM
        elif state in states_check and self.__system_states[1] == SystemState.ARM:
            state = SystemState.ARM
        elif state in states_check and self.__system_states[1] in [SystemState.UPDATE_PASSWORD, SystemState.PASSWORD]:
            if state == SystemState.PASSWORD:
                self.__previous_password = self.__current_password
                self.__current_password = [False, None]
                self.__user_input = None
                self.__clear_lcd_row()
            else:
                state = SystemState.UPDATE_PASSWORD
        elif self.__system_states[PREVIOUS] != self.__system_states[CURRENT]:
            self.__system_states[PREVIOUS] = self.__system_states[CURRENT]
        self.__system_states[CURRENT] = state
        self.__execute_keypad_action()

    def __read_keypad_action(self):
        while True:
            self.__user_input = self.__keypad.read_key_pad()
            match self.__user_input:
                case "A":
                    self.__handle_state(SystemState.ARM)
                case "B":
                    self.__handle_state(SystemState.UNARM)
                case "C":
                    self.__handle_state(SystemState.UPDATE_PASSWORD)
                case _:
                    self.__execute_keypad_action()
            sleep(.2)

    def __execute_keypad_action(self):
        match self.__current_password[0], self.__system_states[CURRENT]:
            case True, SystemState.ARM:
                self.__arm_action()
            case True, SystemState.ARMED:
                self.__armed_action()
            case True, SystemState.UNARM:
                self.__unarm_action()
            case True, SystemState.UNARMED:
                self.__unarmed_action()
            case True, SystemState.UPDATE_PASSWORD:
                self.__update_password_action()
            case _, _:
                self.__set_password_action()

    def __arm_action(self):
        match self.__system_states:
            case SystemState.UNARMED, SystemState.ARM:
                self.__security_check("ARM: PASSWORD   ", SystemState.ARMED)
            case _, _:
                self.__handle_state(self.__system_states[PREVIOUS])

    def __armed_action(self):
        self.__clear_lcd_row()
        self.__start_motion_sensor_thread()
        self.__write_lcd_text("ARMED           ")

    def __unarm_action(self):
        match self.__system_states:
            case SystemState.ARMED, SystemState.UNARM:
                self.__security_check("UNARM: PASSWORD ", SystemState.UNARMED)
            case _, _:
                self.__handle_state(self.__system_states[PREVIOUS])

    def __unarmed_action(self):
        self.__clear_lcd_row()
        self.__stop_motion_sensor_event.set()
        self.__write_lcd_text("UNARMED         ")
    
    def __set_password_action(self):
        match self.__current_password:
            case False, None:
                text = "ENTER PASSWORD  "
            case False, _:
                text = "CHECK PASSWORD  "
                
        self.__write_lcd_text(text)
        
        if self.__user_input != None:
            is_passw_set = self.__current_password[1] != None
            if self.__user_input in ["A", "B", "C"]:
                self.__user_input = None
                self.__clear_lcd_row()
            elif self.__current_password[1] == None if not is_passw_set else self.__user_input:
                if "_" not in self.__user_input:
                    lcd.write(0, 1, self.__user_input)
                    sleep(1)
                    if not is_passw_set:
                        self.__current_password = [is_passw_set, self.__user_input]
                        self.__clear_lcd_row()
                    elif self.__current_password[1] == self.__user_input:
                        self.__current_password[0] = is_passw_set
                        self.__write_lcd_text("PASSWORD SET    ")
                        lcd.write(0, 1, "".join(map(str, ["*" for letter in self.__user_input])))
                        sleep(1)
                        self.__upd_passw_counter = 0
                        if self.__previous_password[0]:
                            self.__previous_password = [False, None]
                        self.__handle_state(SystemState.ARMED)
                    else:
                        lcd.write(0, 1, "NO MATCH        ")
                        sleep(1)
                        self.__upd_passw_counter += 1
                        if self.__upd_passw_counter == PASSW_MAX_TRIES:
                            lcd.write(0, 1, "SYSTEM RESET    ")
                            sleep(1)
                            self.__upd_passw_counter = 0
                            if self.__previous_password[0]:
                                self.__current_password = self.__previous_password
                                self.__previous_password = [False, None]
                                self.__handle_state(self.__system_states[PREVIOUS])
                            else:
                                self.__current_password = [False, None]
                        self.__clear_lcd_row()
                else:
                    lcd.write(0, 1, "".join(map(str, ["*" for letter in self.__user_input])))

    def __update_password_action(self):
        self.__security_check("UPDATE: PASSWORD", SystemState.PASSWORD)
    
    def stop(self):
        sleep(.2)
        lcd.clear()
        self.__prepare_lcd_led(0, 0)
        self.__read_keypad_action_thread = None
        self.__stop_motion_sensor_event.set()
        self.__keypad.stop_timer()
        self.__pi.stop()

if __name__ == "__main__":
    system = MySecuritySystem()
    try:
        while True:
            sleep(.1)
    except KeyboardInterrupt:
        system.stop()
        print("See you later RPi!")