#!/bin/bash
[ "$UID" -eq 0 ] || { echo "This script must be run as root."; exit 1;}
sudo apt-get install python-pip python-dev python-virtualenv 
targetDirectory=$1
virtualenv --system-site-packages "./$targetDirectory"
source ./$targetDirectory/bin/activate
echo "Choose Python version:"
echo "1 Python 2.7"
echo "2 Python 3.n"
read pythonVersion
case $pythonVersion in
  1) sudo -H pip install --upgrade tensorflow pip;;
  2) sudo -H pip3 install --upgrade tensorflow pip;;
esac
