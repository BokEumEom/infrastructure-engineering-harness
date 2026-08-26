@echo off
setlocal
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0harness" %*
  exit /b %errorlevel%
)
where python >nul 2>nul
if %errorlevel%==0 (
  python "%~dp0harness" %*
  exit /b %errorlevel%
)
echo Python 3 is required by the current Research Preview runtime.
echo Install Python 3, then run: harness.cmd setup
exit /b 2
