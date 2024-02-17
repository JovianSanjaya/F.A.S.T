
import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)  # set GPIO 4 as input


def read_sensor():
    ret = False

    if GPIO.input(4):
        ret = True

    return ret