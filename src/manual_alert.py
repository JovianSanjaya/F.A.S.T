import time
from hal import hal_lcd as LCD
from scdf_tele_notification import scd_notification
import requests
# Callback function invoked when any key on the keypad is pressed
lcd = LCD.lcd()

def alert_to_scdf():
    fire_status = 0
    manual_status = 1
    scd_notification(fire_status, manual_status)
    return manual_status


def cancel_alert():
    lcd.lcd_clear()
    lcd.lcd_display_string('Alert cancelled.', 1)
    time.sleep(2)

def false_alarm():
    lcd.lcd_clear()
    lcd.lcd_display_string('Sending false', 1)
    lcd.lcd_display_string('alarm', 2)
    msg = 'False Alarm'
    chat_id = '2126655284'
    TOKEN = '6669662873:AAEdxVOWbKjOM64_ww7u9FqGsSi1xOLuAzk'
    url_alert = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}'
    print(requests.get(url_alert).json())
