@echo off

if "%1"=="" goto USAGE

python %~dp0smart-blame.py "%1"
goto :eof

:USAGE
echo Usage: smart-blame.bat ^<file-to-blame^>
echo        ^<file-to-blame^>: File-path (absolute or relative) to the file to be
echo                         blamed, which needs to be part of a git repo.
