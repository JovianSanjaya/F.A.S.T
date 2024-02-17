import RPi.GPIO as GPIO


def init():
    GPIO.setmode(GPIO.BCM)  # choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(24, GPIO.OUT)  # set GPIO 24 as output


def set_output(led, level):
    GPIO.output(24, level)