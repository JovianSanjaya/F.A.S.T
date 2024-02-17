import requests
from hal import hal_lcd as LCD
lcd = LCD.lcd()

def scd_notification(fire_status,manual_status):
    if (fire_status == 1) | (manual_status == 1):

        msg = 'Fire Detected'
        chat_id = 'replace with your chat id'
        TOKEN = 'replace with your token'
        url_alert = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}'
        print(requests.get(url_alert).json())
        return msg

    else:
        lcd.lcd_clear()
        lcd.lcd_display_string('Everything is good', 1)
        print('Everything is good')

def main():
    fire_status =0
    manual_status = 0
    scd_notification(fire_status,manual_status)