import face_recognition
import numpy as np
import os

class FaceRecognition:
    def __init__(self, reference_folder="src/Data"):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_reference_images(reference_folder)

    def load_reference_images(self, reference_folder):
        """Charge et encode les visages connus depuis un dossier"""
        for root, _, files in os.walk(reference_folder):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    path = os.path.join(root, file)
                    image = face_recognition.load_image_file(path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        name = os.path.basename(root)  # nom du dossier nom personne
                        self.known_face_names.append(name)
                        print(f"Image chargée : {file} → {name}")
                    else:
                        print(f"Aucun visage détecté dans : {file}")

    def compare_with_database(self, image_path):
        """Compare un visage capture avec la base de données"""
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                print("Aucun encodage trouvé dans la capture")
                return "Inconnu"

            distances = face_recognition.face_distance(self.known_face_encodings, encodings[0])
            print(f"[DEBUG] Distances : {distances}")

            if len(distances) == 0:
                return "Inconnu"

            best_match_index = np.argmin(distances)
            if distances[best_match_index] < 0.70:  # seuil reconnaissance a changer 
                return self.known_face_names[best_match_index]
            else:
                return "Inconnu"
        except Exception as e:
            print(f"Erreur lors de la reconnaissance : {e}")
            return "Inconnu"
