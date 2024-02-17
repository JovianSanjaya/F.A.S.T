import RPi.GPIO as GPIO #import RPi.GPIO module


def init():
    global PWM

    GPIO.setmode(GPIO.BCM) #choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(23,GPIO.OUT) #set GPIO 23 as output

    #Configue GPIO pin 23 as PWM, frequency = 5kHz
    PWM = GPIO.PWM(23, 120)


def set_motor_speed(speed):
    if 0 <= speed <= 100:
        PWM.start(speed)
