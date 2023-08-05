@echo off

echo Cleaning up
rmdir /s /q build
rmdir /s /q dist

echo Building wheel
python setup.py build
python setup.py bdist_wheel
