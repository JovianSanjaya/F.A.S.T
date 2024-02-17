from ultralytics import YOLO
import cv2
import math
import cvzone
import requests
from datetime import datetime  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import webbrowser

# Running real time from webcam
cap = cv2.VideoCapture('fire4.mp4')
model = YOLO('fire.pt')

# Reading the classes
classnames = ['fire']

# Variable to keep track of whether notification and firebase has been sent
notification_sent = False
fire_detected_firebase = False

# Initialize Firebase Admin SDK
cred = credentials.Certificate("replace with your json key")  # Update path to your service account key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'replace with your firebase database url'
})
# Function to open index.html in the default web browser
def open_index_html():
    webbrowser.open('index.html')

def send_telegram_notification():
    global notification_sent
    if not notification_sent:
        msg = 'Fire Detected'
        chat_id = 'repalce with your tele chat id'
        TOKEN = 'replace with your tele token'
        url_alert = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}'
        print(requests.get(url_alert).json())
        notification_sent = True
        return msg
    

def main(fire_detected_firebase):
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        result = model(frame, stream=True)

        # Getting bbox, confidence and class names informations to work with
        for info in result:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                Class = int(box.cls[0])
                if confidence > 50:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                    cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                                    scale=1.5, thickness=2)
                    send_telegram_notification()

                    if not fire_detected_firebase:
                        # Insert time to Firebase only if notification has not been sent
                        ref = db.reference('/Fire Detected')
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        str_date = str(current_time)
                        data = {'time': str_date}
                        ref.push().set(data)
                        fire_detected_firebase = True
                        open_index_html()
                    
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

#call function
main(fire_detected_firebase)




# DONE
# TELE
# TEST TELE
# FIREBASE
# FIRE CAMERA DETECTION
# GRAPH

# NOT DONE
# DOCKER FILE
# TEST CASE FOR MAIN
# CHECKING BASIC MAIN

