#!/bin/bash
sudo apt-get --yes install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0

PYENV = "venv"
if [[ ! -d "$PYENV" ]]; then
    echo "creating python environment - $PYENV"
    python3 -m venv venv
else; then
    echo "$PYENV already exists. Using as virtual environment"
fi
source venv/bin/activate
pip install -r requirements.txt
