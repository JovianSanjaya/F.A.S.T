import requests
import time

def drawing_graph(temp_list):
    last_temp = temp_list[-1]
    print(last_temp)
    if last_temp != -100:
        print('Uploading the value...')
        resp = requests.get('https://api.thingspeak.com/update?api_key=7611WMMSP8FNGURY&field1=%s' % last_temp)
        time.sleep(5)
    else:
        return
