#!/bin/sh

lsof -t -i tcp:8000 | xargs kill -9

VENV_DIR="django_venv"
source $VENV_DIR/bin/activate

python manage.py runserver