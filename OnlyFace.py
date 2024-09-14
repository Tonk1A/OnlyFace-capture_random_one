'''
OnlyFace.py

Usage:
- Press the 'Random (r)' button or press the 'R' key to save a randomly detected face as an image.
- Press the 'Delete (d)' button or press the 'D' key to delete all saved images.
- Press the 'Q' key or close the window to exit the application.

'''

import sys
import os
import random
import cv2
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

# Define desired width and height
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Initialize the camera
video_cap = cv2.VideoCapture(0)

# Set the width and height
video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a directory to save images
SAVED_IMG = "images"
if not os.path.exists(SAVED_IMG):
    os.mkdir(SAVED_IMG)

# Initialize face ID
FACE_ID = 0


def delete_all_files(directory):
    ''' Delete all files in a directory '''
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Create the full file path
        file_path = os.path.join(directory, filename)

        # Try to delete the file
        try:
            # Check if the file is a file or a link
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) # Delete the file

        # Handle errors
        except OSError as e:
            print(f'Failed to delete {file_path}. Reason: {e}') # Print the error

class MyApp(QWidget):
    ''' Main class for the application '''

    def __init__(self):
        super().__init__() # Call the parent constructor
        self.init_ui() # Initialize the UI
        self.timer = QTimer(self) # Create a timer
        self.timer.timeout.connect(self.update_frame) # Connect timeout to the update_frame function
        self.timer.start(30)  # Update frame every 30 ms
        self.setFixedWidth(1280) # Set the width of the window
        self.face_id = self.get_latest_face_id() # Initialize face ID

    def init_ui(self):
        ''' Initialize the UI '''

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label to display the video feed
        self.video_label = QLabel("Camera Feed", self)
        layout.addWidget(self.video_label)

        # Create a button to save a random face
        self.btn_random = QPushButton('Random (r)', self)
        self.btn_random.clicked.connect(self.random_image)
        layout.addWidget(self.btn_random)

        # Create a button to delete all images
        self.btn_delete = QPushButton('Delete (d)', self)
        self.btn_delete.clicked.connect(self.delete_images)
        layout.addWidget(self.btn_delete)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle('Face Detection App')
        self.setGeometry(0, 0, 0, 0)
        self.show()
        
    def get_latest_face_id(self):
        '''
        Retrieves the latest face ID from the saved images directory.
        '''
        face_ids = []
        for filename in os.listdir(SAVED_IMG):
            if filename.startswith("face_") and filename.endswith(".jpg"):
                try:
                    face_id = int(filename.split('_')[1].split('.')[0])
                    face_ids.append(face_id)
                except ValueError:
                    pass
        
        if face_ids:
            return max(face_ids) + 1
        return 1
    def key_press_event(self, event):
        ''' Handle key press events '''

        # If the key is 'R', save a random face
        if event.key() == Qt.Key_R:
            self.random_image()

        # If the key is 'D', delete all images
        elif event.key() == Qt.Key_D:
            self.delete_images()

        # If the key is 'Q', close the application
        elif event.key() == Qt.Key_Q:
            self.close()

    def update_frame(self):
        ''' Update the video feed '''

        # Read the frame from the camera
        ret, frame = video_cap.read()

        # If the frame is read successfully
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            face_count = len(faces) # Count the number of faces

            # Iterate over all faces
            for (x, y, w, h) in faces:
                # Draw a rectangle around the face
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display the number of faces
                cv2.putText(
                    frame,
                    f'Faces: {face_count}',
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert the frame to RGB

            # Create a QImage from the frame
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                QImage.Format_RGB888
            )

            self.video_label.setPixmap(QPixmap.fromImage(image)) # Display the image

    def random_image(self):
        ''' Save a random face as an image '''

        # Read the frame from the camera
        ret, frame = video_cap.read()

        # If the frame isn't read successfully
        if not ret:
            print("Failed to capture image")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        # If faces are detected
        if len(faces) > 0:
            self.face_id += 1
            (x, y, w, h) = random.choice(faces)
            img_name = os.path.join(SAVED_IMG, f"face_{FACE_ID}.jpg")
            face_img = frame[y:y + h, x:x + w]
            cv2.imwrite(img_name, face_img)
            self.show_captured_face(img_name)
            print(f"Image saved as {img_name}")
        else:
            self.video_label.setText("No Face Detected")

    def show_captured_face(self, img_name):
        ''' Display the captured face '''

        # Create the full image path
        img_name = os.path.join(SAVED_IMG, f"face_{FACE_ID}.jpg")

        # Create a dialog to display the image
        dialog = QDialog(self)
        dialog.setWindowTitle("Captured Face")
        layout = QVBoxLayout()
        pixmap = QPixmap(img_name)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)

        # Set the layout
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def delete_images(self):
        ''' Delete all saved images '''

        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            'Delete Confirmation',
            'Are you sure you want to delete all images?', 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        # If the user confirms
        if reply == QMessageBox.Yes:
            delete_all_files(SAVED_IMG)
            self.video_label.setText('No Image')
            print("All images deleted.")

    def close_event(self, event):
        ''' Handle the close event '''

        video_cap.release() # Release the camera
        event.accept() # Close the application

if __name__ == '__main__':
    application = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(application.exec_())
