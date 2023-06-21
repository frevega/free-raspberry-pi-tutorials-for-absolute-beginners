import pigpio
import RPi.GPIO as GPIO
import ADC0834
from RepeatTimer import RepeatTimer
from time import sleep

class Lesson29HW:
    def __init__(
        self,
        pi,
        lightThreshold,
        buzzerPin,
        pirPin
    ):
        # PIGPIO & RPi.GPIO
        self.pi = pi
        GPIO.setmode(GPIO.BCM)
        
        # BUZZER
        self.buzzer = self.prepareBuzzer(buzzerPin)
        
        # PIR
        self.pirPin = self.preparePIR(pirPin)
        
        # ADC CHIP
        ADC0834.setup()
        
        # TIMERS
        self.photoTimer = None
        self.pirTimer = None
        self.checkLightTimer = None
        
        # FLAGS
        self.isAlarmActive = False
        
        # DATA
        self.lightThreshold = lightThreshold
        self.photoValue = None
        self.pirValue = None
        
    def prepareBuzzer(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        buzzer = GPIO.PWM(pin, 400)
        
        return buzzer
    
    def preparePIR(self, pin):
        self.pi.set_mode(pin, pigpio.INPUT)
        
        return pin
    
    def readPhotoResistor(self):
        self.photoValue = ADC0834.getResult()
    
    def readPir(self):
        self.pirValue = self.pi.read(self.pirPin)
        
    def checkLightThreshold(self):
        if self.photoValue != None:
            self.sirenAlarm(self.photoValue <= self.lightThreshold and self.pirValue > 0)
    
    def sirenAlarm(self, isActive):
        self.isAlarmActive = isActive
        if isActive:
            print("MOTION DETECTED", end = "\r")
            self.buzzer.start(50)
            for r in range(5):                    
                for i in range(150, 2000):
                    self.buzzer.ChangeFrequency(i)
                    sleep(.0001)
                for i in range(2000, 150, -1):
                    self.buzzer.ChangeFrequency(i)
                    sleep(.0001)
                sleep(.1)
        else:
            print("               ", end = "\r")
            self.buzzer.stop()
            
    def start(self):
        self.photoTimer = RepeatTimer(.5, self.readPhotoResistor)
        self.photoTimer.start()
        self.pirTimer = RepeatTimer(.5, self.readPir)
        self.pirTimer.start()
        self.checkLightTimer = RepeatTimer(.25, self.checkLightThreshold)
        self.checkLightTimer.start()

    def cleanup(self):
        self.photoTimer.cancel()
        self.pirTimer.cancel()
        self.checkLightTimer.cancel()
        sleep(.3)
        self.pi.stop()
        GPIO.cleanup()
        print("\nSee you later RPi!")

if __name__ == "__main__":
    try:
        lesson = Lesson29HW(
            pi = pigpio.pi(),
            lightThreshold = 30,
            buzzerPin = 21,
            pirPin = 12
        )
        lesson.start()
        while True:
            sleep(1)
    except KeyboardInterrupt:
        lesson.cleanup()
