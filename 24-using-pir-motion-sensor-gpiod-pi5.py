import gpiod
from RepeatTimer import RepeatTimer
from time import sleep

chip = gpiod.Chip("/dev/gpiochip4")
sensor_line = chip.get_line(18)
sensor_line.request(consumer = "Sensor", type = gpiod.LINE_REQ_DIR_IN)

timer = RepeatTimer(.1, lambda: print(sensor_line.get_value()))
timer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    timer.cancel()
    sensor_line.release()
    print("\nSee ya later, RPi!\n")