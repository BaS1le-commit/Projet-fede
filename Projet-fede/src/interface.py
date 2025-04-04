import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import tempfile
import os
import threading
from src.drone_command import DroneCommand
from src.video_stream import TelloVideoStream
from ultralytics import YOLO
from src.face_recognition import FaceRecognition
from src.presence_logger import PresenceLogger
import signal
import sys



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Interface Drone Tello")
        self.geometry("900x700")

        self.drone = DroneCommand()
        self.video = TelloVideoStream(f"udp://{self.drone.TELLO_IP}:11111")

        self.yolo_model = YOLO("yolov8n.pt")
        self.face_recognition = FaceRecognition(reference_folder="src/Data")

     
        self.message_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18))
        self.message_label.pack(pady=5)

        self.video_label = ctk.CTkLabel(self)
        self.video_label.pack(pady=20)

        self.last_detected_name = ""
        self.last_detections = []
        self.frame_count = 0

        self.logger = PresenceLogger()

        # Initialisation du writer vidéo
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output_path = "video_enregistrement.mp4"
        self.video_writer = cv2.VideoWriter(self.output_path, fourcc, 10.0, (640, 480))  # Ajustez la taille si besoin
        signal.signal(signal.SIGINT, self.signal_handler)
        self.update_frame()

    def run_face_match(self, image_path):
        name = self.face_recognition.compare_with_database(image_path)
        print(f"Nom reconnu : {name}")
        self.last_detected_name = name
        if name != "Inconnu":
            self.logger.log_presence(name)
        os.remove(image_path)

    def update_frame(self):
        frame = self.video.get_frame()
        if frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            print("Frame vide ou corrompue, skip")
            self.after(100, self.update_frame)
            return

        self.frame_count += 1

        if self.frame_count % 10 == 0:
            print(f"[FRAME {self.frame_count}] Démarrage detection YOLO et reconnaissance")
            yolo_results = self.yolo_model(frame, conf=0.5)[0]
            detections = []
            for box, cls in zip(yolo_results.boxes.xyxy, yolo_results.boxes.cls):
                if int(cls) == 0: 
                    x1, y1, x2, y2 = map(int, box[:4])
                    detections.append((x1, y1, x2, y2))
            self.last_detections = detections

            if detections:
                x1, y1, x2, y2 = detections[0]
                h, w, _ = frame.shape
                x1 = max(0, min(x1, w - 1))
                x2 = max(0, min(x2, w - 1))
                y1 = max(0, min(y1, h - 1))
                y2 = max(0, min(y2, h - 1))
                face_crop = frame[y1:y2, x1:x2]

                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                    cv2.imwrite(tmp_file.name, face_crop)
                    threading.Thread(target=self.run_face_match, args=(tmp_file.name,), daemon=True).start()

        for (x1, y1, x2, y2) in self.last_detections:
            name = self.last_detected_name if self.last_detected_name else "???"
            color = (0, 255, 0) if name != "Inconnu" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        resized_frame = cv2.resize(frame, (640, 480))  
        self.video_writer.write(resized_frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=frame)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.after(100, self.update_frame)

    def signal_handler(self, sig, frame):
        print("Ctrl+C détecté, fermeture propre en cours...")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        print("Nettoyage des ressources...")
        self.video.release()
        self.video_writer.release()
        self.destroy()

    def on_closing(self):
        self.cleanup()

    def on_closing(self):
        self.video.release()
        self.destroy()
