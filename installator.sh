#!/bin/bash
[ "$UID" -eq 0 ] || { echo "This script must be run as root."; exit 1;}
echo "Determine how to install TensorFlow: "
echo "1 virtualenv"
echo "2 'native' pip"
echo "3 Docker"
read mechanismId
case $mechanismId in
  1) 
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
    ;;
  2)
    sudo apt-get install python-pip python-dev
    echo "Choose Python version: "
    echo "1 Python 2.7"
    echo "2 Python 3.n"
    read pythonVersion
    case $pythonVersion in
      1)
        sudo -H pip uninstall tensorflow
        sudo -H pip install tensorflow 
        ;;
      2)
        sudo -H pip3 uninstall tensorflow
        sudo -H pip3 install tensorflow
        ;;
    esac
    ;;
  3)
    echo "Docker Community Edition for Ubuntu"
    sudo apt-get -y install apt-transport-https ca-certificates curl
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update

    sudo apt-get -y install docker-ce

    sudo docker run hello-world

    echo "Select how you want to use TensorFlow: "
    echo "1 If you plan to run TensorFlow programs from the shell"
    echo "2 If you plan to run TensorFlow programs as Jupyter notebooks"
    echo "3 If you'd like to run TensorBoard inside the container"
    read usingMethod
    echo "Copy/paste this URL into your browser and choose Tag Name (without 'gpu' substring in the name)"
    echo "https://hub.docker.com/r/tensorflow/tensorflow/tags/"
    echo "Enter chosen Tag Name:"
    read tagName
    case $usingMethod in
      1) docker run -it gcr.io/tensorflow/tensorflow:$tagName bash;;
      2) docker run -it -p 8888:8888 gcr.io/tensorflow/tensorflow:$tagName;;
      3) docker run -it -p 8888:8888 -p 6006:6006 b.gcr.io/tensorflow:$tagName;; 
    esac
    ;; 
esac


