import pigpio
from time import sleep

def prepareButton(pin: int) -> int:
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_UP)
    
    return pin

def prepareLed(pin: int) -> int:
    pi.set_mode(pin, pigpio.OUTPUT)
    
    return pin

pi = pigpio.pi()
leds = [prepareLed(n) for n in [26, 19, 13]]
buttons = [prepareButton(n) for n in [18, 15, 14]]
buttonStates = [[0, 0] for _ in buttons]
ledStates = [0, 0, 0]

def main():
    while True:
        for index, button in enumerate(buttons):
            buttonStates[index][0] = pi.read(button)
            if buttonStates[index][0] == 0 and buttonStates[index][0] != buttonStates[index][1]:
              pi.write(leds[index], (pi.read(leds[index]) + 1) % 2)
            buttonStates[index][1] = buttonStates[index][0]

try:
    main()
except KeyboardInterrupt:
    _ = [pi.write(n, 0) for n in leds]
    pi.stop()
    print("See ya later!")