import requests

def false_alarm():
    msg = 'False Alarm'
    chat_id = 'replace with your chat id'
    TOKEN = 'replace with your token'
    url_alert = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}'
    print(requests.get(url_alert).json())
    return msg

false_alarm()

