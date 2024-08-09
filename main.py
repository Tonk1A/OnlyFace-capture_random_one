import cv2
import dlib
import os
import numpy as np
from numpy import random

video_cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

saved_img = "images"
if not os.path.exists(saved_img):
    os.makedirs(saved_img)

face_id = 0
face_dict = {}

while True:
    ret, frame = video_cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    
    for face in faces :
        x, y ,w ,h = face.left(), face.top(), face.width(), face.height()
        
        face_detected = False
        for key, value in face_dict.items():
            if abs(x - value[0]) < 50 and abs(y - value[1]) < 50:
                face_id = key
                face_detected = True
                break
            
        if not face_detected:
            face_id = len(face_dict) + 1
            face_dict[face_id] = (x, y)
            imgname = os.path.join(saved_img, f"{face_id}.png")
            cv2.imwrite(imgname, frame[y:y+h, x:x+w])
            
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, str(face_id), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        
    cv2.imshow('Face Capture', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        face_dict.clear()
        face_id = 0
    elif key == ord('r'):
        if len(face_dict) > 0:
            random_id = random.choice(list(face_dict.keys()))
            print(random_id)
        else:
            print("face_dict is empty. Cannot generate a random index.")

            
video_cap.release()
cv2.destroyAllWindows()