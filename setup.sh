#!/bin/bash
sudo apt-get update -y
sudo apt-get --yes install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 libgl1-mesa-glx qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools
sudo apt-get --yes install pycharm-community --classic

DIR="venv"
if [[ ! -d "$DIR" ]]; then
    echo "creating python environment - $DIR"
    python3 -m venv venv
else
    echo "$DIR already exists. Using as virtual environment"
fi
source venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
