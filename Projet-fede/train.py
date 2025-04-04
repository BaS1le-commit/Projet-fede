import os
import torch
import numpy as np
import random
import zipfile
from ultralytics import YOLO

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed()

dataset_dir = "datasets"  #on enregistre les images dans un nv file
os.makedirs(dataset_dir, exist_ok=True)

def unzip_dataset(zip_path, extract_to):
    if os.path.exists(zip_path):
        print(" extraction de {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("extraction termine: {extract_to}")
    else:
        print(f"file introuvable :{zip_path} ")

unzip_dataset("/train.zip", dataset_dir)
unzip_dataset("/valid.zip", dataset_dir)
unzip_dataset("/test.zip", dataset_dir)

def verify_image_labels(image_dir, label_dir):
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"ERREUR: dossier {image_dir} existe pas ")
    if not os.path.exists(label_dir):
        raise FileNotFoundError(f"ERREUR : dossier {label_dir} existe pas ")
    print(f" verif OK : {image_dir} et {label_dir}")

verify_image_labels("/datasets/train/images", "/datasets/train/labels")
verify_image_labels("/datasets/valid/images", "/datasets/valid/labels")

def train(model_path="/yolov10n.pt", data_path="/data.yaml", epochs=32, batch_size=16, img_size=640):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ERREUR : modele {model_path}introuvable")

    model = YOLO(model_path)  
    model.train(
        data=data_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        save=True,
        project="runs",
        name="Vsmodel"
    )
    print("train termine")

train()