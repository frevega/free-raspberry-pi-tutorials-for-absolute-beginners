import ADC0834
import LCD1602
import pigpio
from pigpio_dht import DHT11
from RepeatTimer import RepeatTimer
from time import sleep
from enum import Enum
import RPi.GPIO as GPIO

class Lesson28: 
    def __init__(
        self,
        pi,
        tempThreshold: float,
        LCDAddress: int,
        LCDLedPin: int,
        DHTPin: int,
        buzzerPin: int,
        buttonPins: [int]
    ):
        # PIGPIO & RPi.GPIO
        self.pi = pi
        GPIO.setmode(GPIO.BCM)
        
        # BUTTON PINS
        self.buttonPins = [self.prepareButton(pin) for pin in buttonPins]
        
        # BUTTON STATES MATRIX
        self.buttonStates = [[0, 1], [0, 1]]
        
        # BUZZER
        self.buzzer = self.prepareBuzzer(buzzerPin)
        
        # LCD SCREEN
        self.LCDLedPin = LCDLedPin
        LCD1602.init(LCDAddress)
        
        # ADC CHIP
        ADC0834.setup()
        
        # DHT11
        self.dht = DHT11(DHTPin)
        self.prepareLCDLed(self.LCDLedPin)
        
        # TIMERS
        self.potTimer = None
        self.buttonTimer = None
        self.checkTempTimer = None
        
        # FLAGS
        self.isCelcius = True
        self.isProgramming = False
        self.isAlarmActive = False
        
        # DATA
        self.tempThreshold = tempThreshold
        self.read = [{"valid": False}, {"valid": False}]
        
    def prepareButton(self, pin):
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_UP)
        
        return pin
        
    def prepareBuzzer(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        buzzer = GPIO.PWM(pin, 400)
        
        return buzzer
    
    def prepareLCDLed(self, LCDLedPin): 
        self.pi.set_PWM_dutycycle(self.LCDLedPin, 0)
        self.pi.set_PWM_frequency(self.LCDLedPin, 1000)
        
    def getDHTRead(self) -> str:
        self.read[0] = self.dht.read()
        if self.read[0]["valid"]:
            self.read[1] = self.read[0]
    
    def writeLCD(self):
        if self.isProgramming:
            self.writeProgramming()
        else:
            self.writeTemperature()
    
    def writeProgramming(self):
        LCD1602.write(0, 0, "ALARM PROG MODE")
        LCD1602.write(
            0,
            1,
            f"TEMP >= " \
            f"{format(self.tempThreshold if self.isCelcius else self.tempThreshold * 9/5 + 32, '.1f')}" \
            f"{chr(223)}{'C' if self.isCelcius else 'F'}   "
        )
    
    def writeTemperature(self):
        reading = [read for read in self.read if read["valid"] == True]
        if len(reading) == 0:
            LCD1602.write(0, 0, "Waiting for     ")
            LCD1602.write(0, 1, "Sensor data...  ")
        else:
            LCD1602.write(
                0,
                0,
                f"{'ALARM! ' if self.isAlarmActive else 'Temp '}" \
                f"{reading[0]['temp_c' if self.isCelcius else 'temp_f']}" \
                f"{chr(223)}{'C' if self.isCelcius else 'F'}          "
            )
            LCD1602.write(0, 1, f"Humidity {reading[0]['humidity']}%    ")
    
    def MAP(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def readPot(self):
        self.pi.set_PWM_dutycycle(self.LCDLedPin, ADC0834.getResult())
        
        if self.isProgramming == True:
            self.tempThreshold = self.MAP(ADC0834.getResult(1), 0, 255, 0, 50)
    
    def readButton(self):
        for index, pin in enumerate(self.buttonPins):
            self.buttonStates[index][0] = self.pi.read(pin)
            if self.buttonStates[index][0] == 1 \
               and self.buttonStates[index][0] != self.buttonStates[index][1]:
                if index == 0:
                    self.isCelcius = not self.isCelcius
                else:
                    self.isProgramming = not self.isProgramming
            self.buttonStates[index][1] = self.buttonStates[index][0]
        self.writeLCD()
        
    def checkTempThreshold(self):
        print(GPIO.input(22), end = "\r")
        reading = [read for read in self.read if read["valid"] == True]
        shouldActivateAlarm = not self.isProgramming \
            and len(reading) > 0 \
            and self.tempThreshold <= float(reading[0]["temp_c"])
        self.sirenAlarm(shouldActivateAlarm)
            
    def sirenAlarm(self, isActive):
        self.isAlarmActive = isActive
        if isActive:
            self.buzzer.start(50)
            for i in range(150, 2000):
                self.buzzer.ChangeFrequency(i)
                sleep(.0001)
            for i in range(2000, 150, -1):
                self.buzzer.ChangeFrequency(i)
                sleep(.0001)
        else:
            self.buzzer.stop()
        
    def getInfo(self):
        self.potTimer = RepeatTimer(.01, lesson.readPot)
        self.potTimer.start()
        self.buttonTimer = RepeatTimer(.05, self.readButton)
        self.buttonTimer.start()
        self.checkTempTimer = RepeatTimer(.25, self.checkTempThreshold)
        self.checkTempTimer.start()
        while True:
            self.getDHTRead()
            sleep(1)

    def cleanup(self):
        self.potTimer.cancel()
        self.buttonTimer.cancel()
        self.checkTempTimer.cancel()
        sleep(.3)
        self.pi.stop()
        GPIO.cleanup()
        LCD1602.clear()
        print("\nSee you later RPi!")

if __name__ == "__main__":
    try:
        lesson = Lesson28(
            pi = pigpio.pi(),
            tempThreshold = 25,
            LCDAddress = 0x27,
            LCDLedPin = 21,
            DHTPin = 19,
            buzzerPin = 22,
            buttonPins = [23, 25]
        )
        lesson.getInfo()
    except (KeyboardInterrupt, TimeoutError) as e:
        print(e)
        lesson.cleanup()


