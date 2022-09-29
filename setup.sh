#!/bin/bash
sudo apt-get update
sudo apt-get --yes install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0

DIR = "venv"
if [[ ! -d "$DIR" ]]; then
    echo "creating python environment - $DIR"
    python3 -m venv venv
else; then
    echo "$DIR already exists. Using as virtual environment"
fi
source venv/bin/activate
pip install -r requirements.txt
