import time
from threading import Thread
import queue
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from resident_alerts import fire_detection
from manual_alert import false_alarm
from manual_alert import cancel_alert
from manual_alert import alert_to_scdf
import scdf_tele_notification
from display_graph import drawing_graph

# Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()
lcd = LCD.lcd()


# Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def initialization():
    # initialization of HAL modules
    buzzer.init()
    ir_sensor.init()
    servo.init()
    temp_humid_sensor.init()
    led.init()

    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    lcd = LCD.lcd()
    lcd.lcd_clear()


def main():
    initialization()
    manual_alert_thread = Thread(target=manual_alert_system)
    manual_alert_thread.start()

    while True:
        result = fire_detection()
        drawing_graph(result)

def manual_alert_system():
    lcd.lcd_clear()
    lcd.lcd_display_string('1.Activate alert', 1)
    lcd.lcd_display_string('2.Cancel alert', 2)
    keyvalue = shared_keypad_queue.get()
    print("key value ", keyvalue)
    if keyvalue == 1:
        alert_to_scdf()
        lcd.lcd_clear()
        lcd.lcd_display_string('Send false alarm?', 1)
        lcd.lcd_display_string('1. Yes 2. No', 2)
        input_key = shared_keypad_queue.get()
        print("key value ", input_key)
        if input_key == 1:
            false_alarm()
            repeat()
            return 1

        elif input_key == 2:
            lcd.lcd_clear()
            lcd.lcd_display_string("Alert remains.", 1)
            time.sleep(3)
            repeat()
            return 1
    elif keyvalue == 2:
        cancel_alert()
        repeat()
        return 1
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string('Invalid choice.', 1)
        lcd.lcd_display_string('Choose 1 or 2', 2)
        repeat()
        return 1

def repeat():
    while True:
        manual_alert_system()
        return 1


if __name__ == '__main__':
    main()