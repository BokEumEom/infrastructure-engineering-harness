@echo off
setlocal
where py >nul 2>nul
if %errorlevel%==0 goto use_py
where python >nul 2>nul
if %errorlevel%==0 goto use_python
echo Python 3 is required by the current Research Preview runtime.
echo Install Python 3, then run: harness.cmd setup
exit /b 2

:use_py
py -3 "%~dp0harness" %*
exit /b %errorlevel%

:use_python
python "%~dp0harness" %*
exit /b %errorlevel%
