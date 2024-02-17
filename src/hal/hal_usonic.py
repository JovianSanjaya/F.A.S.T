import RPi.GPIO as GPIO
import time



def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # GPIO25 as Trig
    GPIO.setup(25, GPIO.OUT)

    # GPIO27 as Echo
    GPIO.setup(27, GPIO.IN)


#define a function called distance below:
def get_distance():
    #produce a 10us pulse at Trig
    GPIO.output(25,1)
    time.sleep(0.00001)
    GPIO.output(25,0)

    #measure pulse width (i.e. time of flight) at Echo
    StartTime=time.time()
    StopTime=time.time()
    while GPIO.input(27)==0:
        StartTime=time.time() #capture start of high pulse
    while GPIO.input(27)==1:
        StopTime=time.time() #capture end of high pulse
    ElapsedTime=StopTime-StartTime

    #compute distance in cm, from time of flight
    Distance=(ElapsedTime*34300)/2
       #distance=time*speed of ultrasound,
       #/2 because to & fro
    return Distance




#while (True):
#    print("Measured distance = {0:0.1f} cm".format(get_distance()))
#    time.sleep(1)
