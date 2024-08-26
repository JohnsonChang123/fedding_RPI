#!/bin/bash
cd /home/pi/Desktop/NTOU_CSE_LAB403/main/video;
sudo -u pi nohup python -u /home/pi/Desktop/NTOU_CSE_LAB403/main/video/recording_perSecond.py >> /home/pi/Desktop/NTOU_CSE_LAB403/main/log/savepersec.log &
