apt-get --yes install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0

PYENV = "venv"
if [[ ! -e $PYENV ]]; then
    python3 -m venv venv
elif [[ ! -d $PYENV ]]; then
    echo "$PYENV already exists but is not a directory"
fi
source venv/bin/activate
pip install -r requirements.txt
