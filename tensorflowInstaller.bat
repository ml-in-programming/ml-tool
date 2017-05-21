@echo off
set homeDir=%cd%
call pythonInstaller.bat
cd %homeDir%
@echo Determine how to install TensorFlow. We recommended virtualenv mechanism: 
@echo 1 'native' pip
@echo 2 Anaconda
set /p id=""
if %id% equ 1 (
  call installingWithPip.bat
) else (
  call downloadAndConfigureAnaconda.bat
  cd %homeDir%
  call installJupyter.bat
  call installScipy.bat
  call installTensorflow.bat
  call deactivateEnv.bat
)
@echo TensorFlow successfully installed
