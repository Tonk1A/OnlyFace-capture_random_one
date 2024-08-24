import sys
import cv2
import dlib
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt


video_cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

saved_img = "images"
if not os.path.exists(saved_img):
    os.makedirs(saved_img)

face_id = 0


def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # อัปเดตเฟรมทุก ๆ 30 ms

    def initUI(self):
       
        layout = QVBoxLayout()

        
        self.video_label = QLabel("Camera Feed", self)
        layout.addWidget(self.video_label)

        
        self.btn_random = QPushButton('Random (r)', self)
        self.btn_random.clicked.connect(self.random_image)
        layout.addWidget(self.btn_random)

        
        self.btn_delete = QPushButton('Delete (d)', self)
        self.btn_delete.clicked.connect(self.delete_images)
        layout.addWidget(self.btn_delete)

      
        self.setLayout(layout)

       
        self.setWindowTitle('Face Detection App')
        self.setGeometry(300, 300, 600, 500)
        self.show()

    def keyPressEvent(self, event):
       
        if event.key() == Qt.Key_R:
            self.random_image()
        elif event.key() == Qt.Key_D:
            self.delete_images()
        elif event.key() == Qt.Key_Q:
            self.close()

    def update_frame(self):
        ret, frame = video_cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            
        
            face_count = len(faces)
            
            for i, face in enumerate(faces):
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f'Faces: {face_count}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def random_image(self):
        ret, frame = video_cap.read()
        if not ret:
            print("Failed to capture image")
            return
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        if faces:
            global face_id
            face_id += 1
            
            # สุ่มเลือกใบหน้า
            face = random.choice(faces)
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            img_name = os.path.join(saved_img, f"face_{face_id}.jpg")

            face_img = frame[y:y + h, x:x + w]
            cv2.imwrite(img_name, face_img)

            
            self.show_captured_face(img_name)
            print(f"Image saved as {img_name}")
        else:
            self.video_label.setText("No Face Detected")

    def show_captured_face(self, img_name):
        dialog = QDialog(self)
        dialog.setWindowTitle("Captured Face")
        
        layout = QVBoxLayout()

    
        pixmap = QPixmap(img_name)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec_()

    def delete_images(self):
        reply = QMessageBox.question(self, 'Delete Confirmation', 
                                     'Are you sure you want to delete all images?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            delete_all_files(saved_img)
            self.video_label.setText('No Image')
            print("All images deleted.")
        else:
            pass

    def closeEvent(self, event):
        video_cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
