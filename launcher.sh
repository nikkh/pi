#!/bin/sh
#launcher.sh
# navigate home, then back here and then home again
cd /
cd home/pi/Documents/pi
echo "install service bus" > /home/pi/logs/startup.log
pip install azure.servicebus > /home/pi/logs/install.log
echo "publish my ip address" > /home/pi/logs/startup.log
python ipaddr.py > /home/pi/logs/ipaddr.log
echo "monitor for pi control messages" > /home/pi/logs/startup.log
python piservicebusclient.py > /home/pi/logs/piservicebusclient.log
cd /
