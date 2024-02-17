import RPi.GPIO as GPIO #import RPi.GPIO module
from time import sleep

def init():
    GPIO.setmode(GPIO.BCM) #choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(22,GPIO.IN) #set GPIO 22 as input


def read_slide_switch():
    ret = 0

    if GPIO.input(22):
        ret = 1

    return ret


