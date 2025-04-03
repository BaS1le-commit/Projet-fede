import os
import torch
import numpy as np
import random
import zipfile
from ultralytics import YOLO

# Fixe la seed pour la reproductibilité
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed()

# Dossiers dans lesquels on va extraire les datasets
dataset_dir = "/content/datasets"
os.makedirs(dataset_dir, exist_ok=True)

# Fonction pour dézipper les datasets
def unzip_dataset(zip_path, extract_to):
    if os.path.exists(zip_path):
        print(f"📦 Extraction de {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extraction terminée : {extract_to}")
    else:
        print(f"⚠ Fichier introuvable : {zip_path} (Vérifiez son emplacement)")

# Décompression des datasets (depuis /content)
unzip_dataset("/content/train.zip", dataset_dir)
unzip_dataset("/content/valid.zip", dataset_dir)
unzip_dataset("/content/test.zip", dataset_dir)

# Fonction pour vérifier les fichiers images/labels
def verify_image_labels(image_dir, label_dir):
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"ERREUR : Le dossier {image_dir} n'existe pas !")
    if not os.path.exists(label_dir):
        raise FileNotFoundError(f"ERREUR : Le dossier {label_dir} n'existe pas !")
    print(f"✅ Vérification OK : {image_dir} et {label_dir}")

# Vérifie les datasets après extraction
verify_image_labels("/content/datasets/train/images", "/content/datasets/train/labels")
verify_image_labels("/content/datasets/valid/images", "/content/datasets/valid/labels")

# Fonction d'entraînement
def train(model_path="/content/yolov10n.pt", data_path="/content/data.yaml", epochs=32, batch_size=16, img_size=320):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ERREUR : Le modèle {model_path} est introuvable !")

    model = YOLO(model_path)  # Charge YOLOv10
    model.train(
        data=data_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        save=True,
        project="runs",
        name="Vsmodel"
    )
    print("✅ Entraînement terminé avec succès !")

# Exécution de l'entraînement
train()