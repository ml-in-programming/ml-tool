set homeDir=%cd%
call pythonInstaller.bat
cd %homeDir%
start installingWithPip.bat
echo "TensorFlow successfully installed"