#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

# Anydesk
sudo apt install libgles-dev libegl-dev
sudo ln -s /usr/lib/arm-linux-gnueabihf/libGLESv2.so /usr/lib/libbrcmGLESv2.so
sudo ln -s /usr/lib/arm-linux-gnueabihf/libEGL.so /usr/lib/libbrcmEGL.so

# opencv
sudo apt-get install python3-opencv

# mysql
pip3 install mysql-connector-python

# pandas
sudo apt-get install python3-pandas

# Arduino
sudo apt-get install arduino

# schedule
sudo apt-get ubustall python-schedule

# chmod +x install_libraries.sh
# yes | ./install_libraries.sh