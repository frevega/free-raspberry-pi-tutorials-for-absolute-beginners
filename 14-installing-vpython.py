import pigpio
from threading import Timer
from time import sleep
from vpython import *

class RPiLesson12HW:
    MAX_DUTY = 255.0
    BASE_LED_VALUE = 1.85095
    pi = None
    buttonStates = [[]]
    buttonPushes = []
    ledValues = []
    timer = None

    def __init__(self, leds: list[int], buttons: list[int]):
        self.pi = pigpio.pi()
        
        self.leds = [self.preparePWMLed(n) for n in leds]
        self.buttons = [self.prepareButton(n) for n in buttons]
        self.buttonStates = [[0, 0] for _ in buttons]
        self.buttonPushes = [0 for _ in buttons]
        self.ledValues = [0 for _ in buttons]
 
    def prepareButton(self, pin: int) -> int:
        self.pi.set_mode(pin, pigpio.INPUT)
        self.pi.set_pull_up_down(pin, pigpio.PUD_UP)
        
        return pin

    def preparePWMLed(self, pin: int) -> int:
        self.pi.set_PWM_dutycycle(pin, 0)
        self.pi.set_PWM_frequency(pin, 1000)
        
        return pin

    def run(self):
        for index, button in enumerate(self.buttons):
            self.buttonStates[index][0] = self.pi.read(button)
            
            if self.buttonStates[index][0] == 0 \
               and self.buttonStates[index][0] != self.buttonStates[index][1]:
                
                self.ledValues[index] = int(self.BASE_LED_VALUE ** self.buttonPushes[index])
                self.buttonPushes[index] += 1
                
                if self.ledValues[index] > self.MAX_DUTY:
                    self.ledValues[index] = 0
                    self.buttonPushes[index] = 0
                
                self.pi.set_PWM_dutycycle(self.leds[index], self.ledValues[index])
                
            self.buttonStates[index][1] = self.buttonStates[index][0]
        self.timer = Timer(.1, self.run)
        self.timer.start()

    def deinit(self):
        _ = [self.pi.write(n, 0) for n in self.leds]
        self.timer.cancel()
        self.pi.stop()

if __name__ == "__main__":
    try:
        homework = RPiLesson12HW(
            leds = [26, 19, 13],
            buttons = [18, 15, 14]
        )
        homework.run()
        
        mySphere = sphere(
            radius = 1,
            pos = vector(0, 2, 0),
            axis = vector(0, 1, 0)
        )
        myCylinder = cylinder(
            radius = 1,
            length = 2,
            axis = vector(0, 1, 0)
        )
        myCylinderBase = cylinder(
            radius = 1.15,
            length = .2,
            axis = vector(0, 1, 0)
        )
        legOne = box(
            size = vector(.2, 6, .2),
            color = vector(.2, .2, .2),
            pos = vector(-.50, -1, 0)
        )
        legTwo = box(
            size = vector(.2, 7, .2),
            color = vector(.2, .2, .2),
            pos = vector(.50, -1, 0)
        )
        #rate(100)
        while True:
            mySphere.color = vector(
                homework.buttonPushes[0]/10,
                homework.buttonPushes[1]/10,
                homework.buttonPushes[2]/10            
            )
            myCylinder.color = mySphere.color
            myCylinderBase.color = mySphere.color
            print(f"R: {homework.ledValues[0]:03} - {homework.buttonPushes[0]/10} \tG: {homework.ledValues[1]:03} - {homework.buttonPushes[1]/10} \tB: {homework.ledValues[2]:03} - {homework.buttonPushes[2]/10}", end = "\r")
            sleep(.1)
    except KeyboardInterrupt:
        homework.deinit()
        print("\nSee ya later, RPi!")


