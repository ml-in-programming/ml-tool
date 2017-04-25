#!/bin/bash

[ "$UID" -eq 0 ] || { echo -e "This script must be run as root.\nFor example: sudo ./installator.sh"; exit 1;}
set -u

function choosePythonVersion 
{
  echo "Choose Python version. If you don't know input 1: "
  echo "1 Python 2.7"
  echo "2 Python 3.x"
  read pythonVersion
  while [[ $pythonVersion -lt 1 || $pythonVersion -gt 2 ]]
  do  
    echo "Select one of the options"
    read pythonVersion
  done    
}

function chooseInstallationMechanism
{
  echo "Determine how to install TensorFlow. We recommended virtualenv mechanism: "
  echo "1 virtualenv"
  echo "2 'native' pip"
  echo "3 Docker"
  echo "4 Anaconda"
  read mechanismId
  while [[ $mechanismId -lt 1 || $mechanismId -gt 4 ]]
  do  
    echo "Select one of the options"
    read mechanismId
  done
}

function checkForPip3Existence
{
  if ! pip3Loc="$(type -p "pip3")" || [ -z "$pip3Loc" ]; then
    apt-get -y install python3-pip
  fi
}

function cudaToolkitInstallation
{
  apt-get install linux-headers-$(uname -r)
  wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb"
  dpkg -i $(locate -b "\cuda-repo-*.deb")
  apt-get install cuda

  export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}
  if [ "$(uname -m)" == "x86_64" ]; then
    export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
  else 
    export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
  fi
}

function cuDNNInstallation
{
  #registration
  wget "https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v5.1/prod_20161129/8.0/cudnn-8.0-linux-x64-v5.1-tgz"
  cd ~
  tar -zxf ./Downloads/cudnn-8.0-linux-x64-v5.1.tgz
  cd cuda
  cp lib64/* /usr/local/cuda/lib64/
  cp include/* /usr/local/cuda/include/
  printf 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"\nexport CUDA_HOME=/usr/local/cuda' >> ~/.bashrc
}

function nvidiaSoftwareInstallation
{
  cudaToolkitInstallation
  cuDNNInstallation
}

echo "Determine which TensorFlow to install. If you don't know input 1: "
echo "1 TensorFlow with CPU support only"
echo "2 TensorFlow with GPU support only"
read processingUnit
if [ $processingUnit == 2 ]; then
  nvidiaSoftwareInstallation
fi

echo "Determine how to install TensorFlow. We recommended virtualenv mechanism: "
echo "1 virtualenv"
echo "2 'native' pip"
echo "3 Docker"
echo "4 Anaconda"
read mechanismId
while [[ $mechanismId -lt 1 || $mechanismId -gt 4 ]]
do  
  echo "Select one of the options"
  read mechanismId
done

case $mechanismId in
  1) 
    echo "Install TensorFlow with virtualenv mechanism"
    apt-get -y install python-pip python-dev python-virtualenv 
    echo "Input target directory that specifies the top of the virtualenv tree. For example './tensorflow'"
    read targetDirectory
    virtualenv --system-site-packages $targetDirectory
    source ./$targetDirectory/bin/activate

    choosePythonVersion
    case $pythonVersion in
      1) pip install --upgrade tensorflow pip;;
      2) 
        checkForPip3Existence
        pip3 install --upgrade tensorflow pip
        ;;
    esac
    ;;
  2)
    echo "Install TensorFlow with native pip mechanism"
    apt-get install python-pip python-dev
    choosePythonVersion
    case $pythonVersion in
      1) pip install tensorflow;;
      2) 
        checkForPip3Existence
        pip3 install tensorflow
        ;;
    esac
    ;;
  3)
    echo "Install TensorFlow with Docker Community Edition for Ubuntu mechanism"
    apt-get -y install apt-transport-https ca-certificates curl
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update

    apt-get -y install docker-ce

    echo "Select how you want to use TensorFlow. If you don't know input 1: "
    echo "1 If you plan to run TensorFlow programs from the shell"
    echo "2 If you plan to run TensorFlow programs as Jupyter notebooks"
    echo "3 If you'd like to run TensorBoard inside the container"
    read usingMethod
    while [[ $usingMethod -gt 4 || $usingMethod -lt 1 ]]
    do  
      echo "Select one of the options"
      read usingMethod
    done    
    echo "Copy/paste this URL into your browser and choose Tag Name (without 'gpu' substring in the name)"
    echo "https://hub.docker.com/r/tensorflow/tensorflow/tags/"
    echo "Input chosen Tag Name, if you don't know input 'latest-py3'"
    read tagName
    case $usingMethod in
      1) docker run -it gcr.io/tensorflow/tensorflow:$tagName bash;;
      2) docker run -it -p 8888:8888 gcr.io/tensorflow/tensorflow:$tagName;;
      3) docker run -it -p 8888:8888 -p 6006:6006 b.gcr.io/tensorflow:$tagName;; 
    esac
    ;; 
  4)
    echo "Install TensorFlow with Anaconda mechanism"
    processorArchitecture=$(uname -i)
    cd /home/$SUDO_USER/Downloads/
    choosePythonVersion
    case $pythonVersion in
      1) 
        case $processorArchitecture in
          "x86_64") 
            wget "https://repo.continuum.io/archive/Anaconda2-4.3.1-Linux-x86_64.sh"
            bash Anaconda2-4.3.1-Linux-x86_64.sh
            ;;
          "i386") 
            wget "https://repo.continuum.io/archive/Anaconda2-4.3.1-Linux-x86.sh"
            bash Anaconda2-4.3.1-Linux-x86.sh
            ;;
        esac
        ;;
      2) 
        case $processorArchitecture in 
          "x86_64") 
            wget "https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh"
            bash Anaconda3-4.3.1-Linux-x86_64.sh
            ;;
          "i386") 
            wget "https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86.sh"
            bash Anaconda3-4.3.1-Linux-x86.sh
            ;;
        esac
        ;;
    esac
    ;;
esac




