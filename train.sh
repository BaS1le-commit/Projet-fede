#!/bin/bash
 
echo "Activation de l'environnement virtuel..."
source venv/bin/activate
 
echo "Lancement de l'entraînement du modèle..."
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
REAL_PATH="$SCRIPT_DIR/Projet-fede/train.py"
 
echo "Chemin absolu de flaskApi.py : $REAL_PATH"
 
# Exécuter flaskApi.py avec Python
python "$REAL_PATH"
