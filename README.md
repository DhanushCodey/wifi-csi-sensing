# wifi-csi-sensing

Noting yet we're cookin🔥, This is just organized


Module - 00

- Setting up the project using git and github
- Organizing files

rquirments and packages : 

brew install python@3.12

/opt/homebrew/bin/python3.12 -m venv .venv

"cd ~/Projects/wifi-csi-sensing
python3 -m venv .venv
source .venv/bin/activate
pip install numpy matplotlib pyserial pyyaml pytest
pip freeze > requirements.txt"

Module - 01

- Hardware inventory 
- Label each board physically (tape, B1–B5). Record chip variant, flash size, serial     port, USB-serial chip. Photograph the boards and the labels.
- Accept: docs/hardware.md lets a stranger identify which physical board is which.

RUN THESE THREE COMMAND :
- source .venv/bin/activate 
- pip install esptool
- pip freeze > requirements.txt


Ask chip What it is : (it get's the detail)
- ls /dev/usbserial.cu*
- esptool.py --port /dev/cu.usbserial-0001 flash_id
