# 1 armed       A
# 2 unarmed     B
# 3 password    C

import LCD1602 as lcd
import pigpio
import os
from enum import Enum
from KeyPad import KeyPad
from pygame import mixer
from RepeatTimer import RepeatTimer
from threading import Event, Thread
from time import sleep

SystemState = Enum("SystemState", ["ARM", "ARMED", "UNARM", "UNARMED", "PASSWORD", "UPDATE_PASSWORD"])

PREVIOUS = 0
CURRENT = 1
PASSW_MAX_TRIES = 3
MIN_PASSW_LENGTH = 4
MAX_PASSW_LENGTH = 8
SECURITY_CHECK_MAX_TRIES = 1
ARMING_ALARM_OFFSET = 5

class MySecuritySystem:
    def __init__(self):
        self.__user_input = None
        self.__upd_passw_counter = 0
        self.__lcd_text_to_write = [None, None]
        self.__motion_sensor_thread = None
        self.__file_path = "resources/.passw"
        self.__pi = pigpio.pi()
        self.__prepare_lcd()
        self.__prepare_keypad()
        self.__prepare_motion_sensor()
        self.__stop_motion_sensor_event = Event()
        self.__system_states = [None, SystemState.PASSWORD]
        self.__current_password = [False, None]
        self.__previous_password = [False, None]
        self.__prepare_alarm()
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
    
    def __prepare_alarm(self):
        mixer.init()
        mixer.music.load("resources/burglar_alarm.mp3")
        mixer.music.set_volume(0.3)
    
    def __start_alarm(self):
        if not mixer.music.get_busy():
            mixer.music.play(5)

    def __stop_alarm(self):
        if mixer.music.get_busy():
            mixer.music.stop()

    def __start_motion_sensor_thread(self):
         if self.__motion_sensor_thread is None:
            self.__stop_motion_sensor_event.clear()
            self.__motion_sensor_thread = Thread(target = self.__read_motion_sensor, args = (self.__stop_motion_sensor_event,), daemon = True)
            if not self.__motion_sensor_thread.is_alive():
                self.__motion_sensor_thread.start()

    def __read_motion_sensor(self, event):
        while True:
            print(self.__pi.read(self.__motion_sensor_pin))
            if event.is_set():
                self.__stop_alarm()
                self.__motion_sensor_thread = None
                break
            else:
                if self.__pi.read(self.__motion_sensor_pin) == 1:
                    self.__start_alarm()
                sleep(.1)

    def __clear_lcd_row(self, col = 0, row = 1):
        lcd.write(col, row, "".join([" " for space in range(16)]))

    def __write_lcd_text(self, text, col = 0, row = 0):
        self.__lcd_text_to_write[0] = self.__lcd_text_to_write[1]
        self.__lcd_text_to_write[1] = text

        if self.__lcd_text_to_write[0] != self.__lcd_text_to_write[1]:
            lcd.write(col, row, self.__lcd_text_to_write[1])

    def __security_check(self, text, state):
        self.__write_lcd_text(text)
        if self.__user_input in ["A", "B", "C"]:
            self.__user_input = None
            self.__clear_lcd_row()
        elif self.__user_input != None:
            if "_" not in self.__user_input:
                if self.__current_password[1] == self.__user_input:
                    self.__upd_passw_counter = 0
                    if state == SystemState.ARMED:
                        self.__armed_alarm_delay()
                    else:
                        self.__handle_state(state)
                else:
                    lcd.write(0, 1, "NO MATCH        ")
                    sleep(1)
                    self.__update_password_counter(False)
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
        self.__execute_state_action()

    def __read_keypad_action(self):
        while True:
            self.__user_input = self.__keypad.read_key_pad()
            states_check = [SystemState.ARMED, SystemState.UNARMED]
            match self.__user_input:
                case "A":
                    self.__handle_state(SystemState.ARM if self.__system_states[CURRENT] in states_check else self.__system_states[PREVIOUS])
                case "B":
                    self.__handle_state(SystemState.UNARM if self.__system_states[CURRENT] in states_check else self.__system_states[PREVIOUS])
                case "C":
                    self.__handle_state(SystemState.UPDATE_PASSWORD if self.__system_states[CURRENT] in states_check else self.__system_states[PREVIOUS])
                case _:
                    self.__execute_state_action()
            sleep(.2)

    def __execute_state_action(self):
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
        if mixer.music.get_busy():
            self.__write_lcd_text("MOTION DETECTED", row = 1)
        else:  
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
        if self.__system_states[PREVIOUS] == None and self.__check_password_file():
            self.__armed_alarm_delay()
        else:
            match self.__current_password:
                case False, None:
                    text = "ENTER PASSWORD  "
                case False, _:
                    text = "CHECK PASSWORD  "
                    
            self.__write_lcd_text(text)
            
            if self.__user_input != None:
                is_passw_set = self.__current_password[1] != None
                if self.__user_input in ["A", "B", "C"]:
                    # password, none    //  none, password                                              (1) SET PASSWORD WHEN FILE DOES NOT EXIST: DO NOTHING?
                    # password, unarmed //  unarmed, update password    //  update password, unarmed    (2) PREVIOUS & CURRENT STATE IN: UNARMED, ARMED, UPDATE_PASSWORD
                    # password, armed   //  armed, update password      //  update password, armed
                    states_check = [SystemState.UNARMED, SystemState.ARMED, SystemState.UPDATE_PASSWORD]
                    if self.__system_states[PREVIOUS] in states_check or self.__system_states[CURRENT] in states_check: # (2)
                        self.__system_states = [SystemState.PASSWORD, SystemState.ARMED if SystemState.ARMED in self.__system_states else SystemState.UNARMED]
                        self.__current_password = self.__previous_password
                        self.__previous_password = [False, None]
                        self.__handle_state(self.__system_states[CURRENT])
                    else: # (1)
                        self.__user_input = None
                        self.__clear_lcd_row()
                elif self.__current_password[1] == None if not is_passw_set else self.__user_input:
                    if "_" not in self.__user_input:
                        if not MIN_PASSW_LENGTH <= len(self.__user_input) <= MAX_PASSW_LENGTH and not is_passw_set:
                            self.__write_lcd_text("PASSWORD LENGTH:")
                            self.__write_lcd_text(f"{MIN_PASSW_LENGTH} TO {MAX_PASSW_LENGTH} CHARS", row = 1)
                            sleep(2)
                            self.__clear_lcd_row(row = 1)
                            self.__update_password_counter()
                        else:
                            lcd.write(0, 1, self.__user_input)
                            sleep(1)
                            if not is_passw_set:
                                self.__upd_passw_counter = 0
                                self.__current_password = [is_passw_set, self.__user_input]
                                self.__clear_lcd_row()
                            elif self.__current_password[1] == self.__user_input:
                                self.__current_password[0] = is_passw_set
                                self.__write_password_file(self.__user_input)
                                self.__write_lcd_text("PASSWORD SET    ")
                                lcd.write(0, 1, "".join(map(str, ["*" for letter in self.__user_input])))
                                sleep(1)
                                self.__upd_passw_counter = 0
                                if self.__previous_password[0]:
                                    self.__previous_password = [False, None]
                                self.__armed_alarm_delay()
                            else:
                                lcd.write(0, 1, "NO MATCH        ")
                                sleep(1)
                                self.__update_password_counter()
                    else:
                        lcd.write(0, 1, "".join(map(str, ["*" for letter in self.__user_input])))

    def __update_password_counter(self, is_new_passw = True):
        self.__upd_passw_counter += 1
        if self.__upd_passw_counter == PASSW_MAX_TRIES if is_new_passw else SECURITY_CHECK_MAX_TRIES:
            lcd.write(0, 1, "SYSTEM RESET    ")
            sleep(1)
            self.__upd_passw_counter = 0
            if is_new_passw:
                if self.__previous_password[0]:
                    self.__current_password = self.__previous_password
                    self.__previous_password = [False, None]
                    self.__handle_state(self.__system_states[PREVIOUS])
                else:
                    self.__current_password = [False, None]
            else:
                self.__handle_state(self.__system_states[PREVIOUS])
        self.__clear_lcd_row()

    def __armed_alarm_delay(self):
        if self.__system_states[0] != SystemState.ARMED:
            self.__clear_lcd_row()
            counter = 0
            while counter <= ARMING_ALARM_OFFSET:
                screen_counter = ARMING_ALARM_OFFSET - counter
                self.__write_lcd_text("ARMING SYSTEM")
                if screen_counter >= 1:
                    self.__write_lcd_text(f"IN {screen_counter} {'SECONDS   ' if screen_counter > 1 else 'SECOND   '}", row = 1)
                else:
                    self.__write_lcd_text("NOW        ", row = 1)
                counter += 1
                sleep(1)
            self.__handle_state(SystemState.ARMED)

    def __update_password_action(self):
        self.__security_check("UPDATE: PASSWORD", SystemState.PASSWORD)

    def __check_password_file(self):
        try:
            with open(self.__file_path) as file:
                self.__current_password = [True, file.read()]
                
                return True
        except FileNotFoundError:
            return False

    def __write_password_file(self, password):
        with open(self.__file_path, "w") as file:
            file.write(password)

    def stop(self):
        sleep(.2)
        lcd.clear()
        self.__stop_alarm()
        self.__prepare_lcd_led(0, 0)
        self.__stop_motion_sensor_event.set()
        self.__read_keypad_action_thread = None
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