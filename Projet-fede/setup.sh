#!/bin/bash

echo "Setup Python 3.9 sur Kali Linux..."

sudo apt update && sudo apt upgrade -y

if ! command -v python3.9 &> /dev/null; then
    echo "Python 3.9 non trouvé. Compilation et installation..."

    sudo apt install -y wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev curl libbz2-dev

    cd /tmp
    wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz
    tar -xf Python-3.9.18.tgz
    cd Python-3.9.18
    ./configure --enable-optimizations
    make -j$(nproc)
    sudo make altinstall  

    echo "Python 3.9 installé"
else
    echo "Python 3.9 déjà installé : $(python3.9 --version)"
fi

if [ ! -d "venv" ]; then
    echo "Environnement virtuel non trouvé. Création avec Python 3.9..."
    python3.9 -m venv venv
else
    echo "Environnement virtuel détecté."
fi

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installation des dépendances Python..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Fichier requirements.txt non trouvé !"
    exit 1
fi

echo "Setup Python 3.9 terminé avec succès !"
