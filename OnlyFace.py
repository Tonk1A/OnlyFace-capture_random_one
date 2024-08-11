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

def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

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
            imgname = os.path.join(saved_img, f"face_{face_id}.png")
            cv2.imwrite(imgname, frame[y:y+h, x:x+w])
            
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, str(face_id), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        
    cv2.imshow('Face Capture', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        delete_all_files(saved_img)
        break
    elif key == ord('c'):
        delete_all_files(saved_img)
        face_dict.clear()
        face_id = 0
    elif key == ord('r'):
        if len(face_dict) > 0:
            path = os.path.join(os.path.dirname(__file__), 'images')
            img_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            random_id = random.choice(img_files)
            img_path = os.path.join(path, random_id)
            image = cv2.imread(img_path)
            cv2.imshow('Random Face', image)
        else:
            print("no face have been captured yet.")

            
video_cap.release()
cv2.destroyAllWindows()