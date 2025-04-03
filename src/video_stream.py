import cv2
import threading
import time

class TelloVideoStream:
    def __init__(self, video_url):
        self.cap = cv2.VideoCapture(video_url)

        if not self.cap.isOpened():
            print("Impossible d'ouvrir le flux vidéo. Verifie la connexion au Tello")
        else:
            print("Flux video ouvert avec succes")

        self.frame = None
        self.running = True

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()

            if ret:
                self.frame = frame

            else: 
                time.sleep(0.1) 

    def get_frame(self):
        try:
            return self.frame.copy() if self.frame is not None else None
        except Exception as e:
            print(f"Erreur recuperation frame : {e}")
            return None

    def release(self):
   
        self.running = False
        if self.cap:
            self.cap.release()
