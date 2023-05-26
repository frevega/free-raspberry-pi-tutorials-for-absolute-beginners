import ADC0834
import LCD1602
import pigpio
from pigpio_dht import DHT11
from RepeatTimer import RepeatTimer
from time import sleep

class Lesson25:
    def __init__(
        self,
        pi,
        LCDAddress: int,
        LCDLedPin: int,
        DHTPin: int,
        buttonPin: int
    ):
        self.pi = pi
        self.buttonPin = buttonPin
        self.pi.set_mode(buttonPin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.buttonPin, pigpio.PUD_UP)
        self.buttonStates = [0, 1]
        self.isCelcius = True
        self.LCDLedPin = LCDLedPin
        LCD1602.init(LCDAddress)
        ADC0834.setup()
        self.dht = DHT11(DHTPin)
        self.prepareLCDLed(self.LCDLedPin)
        self.potTimer = None
        self.buttonTimer = None
        self.read = [{"valid": False}, {"valid": False}]
        
    def prepareLCDLed(self, LCDLedPin): 
        self.pi.set_PWM_dutycycle(self.LCDLedPin, 0)
        self.pi.set_PWM_frequency(self.LCDLedPin, 1000)
        
    def getDHTRead(self) -> str:
        self.read[0] = self.dht.read()
        if self.read[0]["valid"]:
            self.read[1] = self.read[0]
    
    def writeLCD(self):
        reading = [read for read in self.read if read["valid"] == True]
        if len(reading) == 0:
            LCD1602.write(0, 0, "Waiting for     ")
            LCD1602.write(0, 1, "Sensor data...  ")
        else:
            LCD1602.write(0, 0, f"Temp {reading[0]['temp_c' if self.isCelcius else 'temp_f']}{chr(223)}{'C' if self.isCelcius else 'F'}       ")
            LCD1602.write(0, 1, f"Humidity {reading[0]['humidity']}%    ")

    def readPot(self):
        self.pi.set_PWM_dutycycle(self.LCDLedPin, ADC0834.getResult())
    
    def readButton(self):
        self.buttonStates[0] = self.pi.read(self.buttonPin)
        if self.buttonStates[0] == 1 and self.buttonStates[0] != self.buttonStates[1]:
            self.isCelcius = not self.isCelcius
        self.buttonStates[1] = self.buttonStates[0]
        self.writeLCD()
        
    def getInfo(self):
        self.potTimer = RepeatTimer(.01, lesson.readPot)
        self.potTimer.start()
        self.buttonTimer = RepeatTimer(.05, self.readButton)
        self.buttonTimer.start()
        while True:
            self.getDHTRead()
            sleep(1)

    def cleanup(self):
        self.potTimer.cancel()
        self.buttonTimer.cancel()
        sleep(.3)
        self.pi.stop()
        LCD1602.clear()
        print("\nSee you later RPi!")

if __name__ == "__main__":
    try:
        lesson = Lesson25(
            pi = pigpio.pi(),
            LCDAddress = 0x27,
            LCDLedPin = 26,
            DHTPin = 19,
            buttonPin = 23
        )
        lesson.getInfo()
    except (KeyboardInterrupt, TimeoutError) as e:
        print(e)
        lesson.cleanup()
