#!/bin/bash
sudo apt-get update && sudo apt-get dist-upgrade -y
sudo apt-get install devscripts debhelper cmake libldap2-dev libgtkmm-3.0-dev libarchive-dev libcurl4-openssl-dev intltool
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0 libgirepository1.0-dev -y
sudo apt install code -y

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
code .
