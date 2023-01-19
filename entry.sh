#!/bin/bash

sudo apt install mysql-server -y
sudo systemctl start mysql.service

source ./venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt -r requirements_dev.txt
python3 app.py