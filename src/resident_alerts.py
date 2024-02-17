
import time
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_sensor
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
from time import sleep
from scdf_tele_notification import scd_notification

temp_list = []
def fire_detection():
    fire_status = 0

    measured_temp = temp_sensor.read_temp_humidity()
    sleep(5)
    temp_list.append(measured_temp[0]) #this list will be shown in the graph
    smoke = ir_sensor.get_ir_sensor_state()
    print("Temperature is", temp_list)
    if measured_temp[0] > 60 or smoke:
        fire_status = 1
    if measured_temp[0] < 60 and not smoke:
        fire_status = 0
    if fire_status == 1:
        led.set_output(1, 1)
        time.sleep(2)
        led.set_output(1, 0)
        time.sleep(2)
        fire_alarm()
        rotate_servo()
        manual_status = 0
        scd_notification(fire_status, manual_status)
    else:
        return temp_list
    return temp_list




def fire_alarm():
    buzzer.init()
    buzzer.turn_on()
    buzzer.beep(0.2,0.1,5)
    buzzer.turn_off()


def rotate_servo():
    servo.init()

    for i in range(0, 180, 5):
        servo.set_servo_position(i)
        sleep(0.05)




