import time
import RPi.GPIO as GPIO


def init():
    GPIO.setmode(GPIO.BCM)  # choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)  # set GPIO 18 as output


def turn_on():
    GPIO.output(18, 1)  # Turn on the buzzer


def turn_off():
    GPIO.output(18, 0)


def turn_on_with_timer(duration):
    GPIO.output(18, 1)  # Turn on the buzzer
    time.sleep(duration)  # Duration to turn on the buzzer
    GPIO.output(18, 0)  # Turn off when time is up


def beep(ontime, offtime, repeatnum):
    for cnt in range(repeatnum):
        GPIO.output(18, 1)
        time.sleep(ontime)
        GPIO.output(18, 0)
        time.sleep(offtime)



