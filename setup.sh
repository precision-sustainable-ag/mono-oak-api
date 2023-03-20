#!/bin/bash
pip install virtualenv
python -m venv testenv
source /home/pi/repos/test/testenv/bin/activate
python install -r requirements.txt
flask run

# run using sudo sh ./setup.sh (might have to run `sudo chmod +x setup.sh`)