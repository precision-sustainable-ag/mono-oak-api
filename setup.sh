#!/bin/bash
sudo apt update
sudo apt upgrade
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
 
wget https://www.python.org/ftp/python/3.8.0/Python-3.9.0.tgz

tar zxf Python-3.9.0.tgz
cd Python-3.9.0
./configure --enable-optimizations
make -j 4
sudo make altinstall

pip install virtualenv
python -m venv testenv
source /home/pi/repos/test/testenv/bin/activate
python install -r requirements.txt
flask run

# run using sudo sh ./setup.sh (might have to run `sudo chmod +x setup.sh`)