import pigpio
from time import sleep

pi = pigpio.pi()
sensor_pin = 23
pi.set_mode(sensor_pin, pigpio.INPUT)

if __name__ == "__main__":
    try:
        while True:
            print(pi.read(sensor_pin))
            sleep(.1)
    except KeyboardInterrupt:
        print("\nSee you later RPi!")