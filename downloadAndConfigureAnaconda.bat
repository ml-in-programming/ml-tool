@echo off
powershell Invoke-WebRequest https://repo.continuum.io/archive/Anaconda3-4.3.1-Windows-x86_64.exe -OutFile C:\Users\%username%\Downloads\Anaconda3-4.3.1-Windows-x86_64.exe
cd C:/Users/%username%/Downloads
Anaconda3-4.3.1-Windows-x86_64.exe
conda create --name tensorflow python=3.5
activate tensorflow
