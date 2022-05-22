#!/bin/sh

VENV_DIR="django_venv"

# setup venv
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

pip  install --force-reinstall -r requirements.txt
