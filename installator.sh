#!/bin/bash
[ "$UID" -eq 0 ] || { echo "This script must be run as root."; exit 1;}
sudo apt-get install python-pip python-dev python-virtualenv 
targetDirectory=$1
virtualenv --system-site-packages "./$targetDirectory"
source ./$targetDirectory/bin/activate
sudo -H pip install --upgrade tensorflow pip
