import cv2
import dlib
import os
import numpy as np
import random
from tkinter import *
from PIL import Image, ImageTk

# Initialize Dlib's face detector
detector = dlib.get_frontal_face_detector()

# Create the directory for saving images if it doesn't exist
saved_img_dir = "images"
if not os.path.exists(saved_img_dir):
    os.makedirs(saved_img_dir)

# Function to delete all files in the images directory
def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Basic Tkinter window setup
root = Tk()
root.title("Face Detection GUI")

# Label to display the video feed
video_label = Label(root)
video_label.pack()

# Variable to control video capture
running = False

# Function to start the video capture
def start_video():
    global video_cap, running
    running = True
    video_cap = cv2.VideoCapture(0)
    update_frame()

# Function to update the video frame
def update_frame():
    if running:
        ret, frame = video_cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Convert the frame to a format Tkinter can work with
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        
        # Schedule the next frame update
        video_label.after(10, update_frame)

# Function to randomly capture and save one detected face image
def random_capture():
    if running and video_cap.isOpened():
        ret, frame = video_cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            if faces:
                face = random.choice(faces)  # Randomly select one face
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                face_img = frame[y:y+h, x:x+w]
                file_name = os.path.join(saved_img_dir, f"face_{random.randint(1000, 9999)}.jpg")
                cv2.imwrite(file_name, face_img)
                print(f"Randomly saved {file_name}")

# Function to stop the video capture
def stop_video():
    global running
    running = False
    video_cap.release()

# Buttons to control the video feed and capture images
start_button = Button(root, text="Start Video", command=start_video)
start_button.pack(side=LEFT, padx=10)

stop_button = Button(root, text="Stop Video", command=stop_video)
stop_button.pack(side=LEFT, padx=10)

random_button = Button(root, text="Random Capture", command=random_capture)
random_button.pack(side=LEFT, padx=10)

delete_button = Button(root, text="Delete All Images", command=lambda: delete_all_files(saved_img_dir))
delete_button.pack(side=LEFT, padx=10)

# Start the Tkinter main loop
root.mainloop()
