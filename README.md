# wifi-csi-sensing

Human's presence sensing project withput using speaker, sensor or camera by via CSI(channel state information) in esp32.

Classes are what the model predicts. Your four, from the plan:

empty room
person seated still
person walking
hand gesture, close range

## Module - 00 - Goal (Focuing on git and github)

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

## Module - 01 - Goal : (PROJECT SETUP)

- Hardware inventory 
- Label each board physically (tape, B1–B5). Record chip variant, flash size, serial     port, USB-serial chip. Photograph the boards and the labels.
- Accept: docs/hardware.md lets a stranger identify which physical board is which.

- esptool -p <port-id> chip-id
- esptool -p <port-id> flash-id
- esptool -p <port-id> read-mac
-  grep -i baud sdkconfig 
   -  to get the baud rate 

## Module - 02 - GOAL : (CHECK HARDWARE)

RUN THESE THREE COMMAND :
- source .venv/bin/activate 
- pip install esptool
- pip freeze > requirements.txt


Ask chip What it is : (it get's the detail)
- ls /dev/usbserial.cu*
- esptool.py --port /dev/cu.usbserial-0001 flash_id

## Module 03 - GOAL : (ESP-IDF(Espressif Iot development famework) (INSTALL)
- brew install cmake ninja dfu-utils
- mkdir -p ~/esp && cd ~/esp
- git clone -b release/v5.5 --recursive https://github.com/espressif/esp-idf.git


cmake (build sys generator) -   the architect turn our code into blue print
ninja (the builder)         -   takes the blueprint and compile and link the code. Has extreme execution speed
dfu-utils (connecter)       -   cmd line program used to upload and download device firmware via usb

=> C++/C code -> cmake(generate build instruction) -> ninja (compiles code into final .bin file) -> dfu-utils (Flasher the bin to the native usb)

C++ -> Cmake -> Ninja -> dfu-util(packet manager)

- mkdir -p ~/esp && cd ~/esp
- git clone -b release/v5.5 --recursive https://github.com/espressif/esp-idf.git

creating a directory and downloading the core esp-idf framework and its dependent libraries.

- cd ~/esp/esp-idf
- ./install.sh esp32

esp32 runs (Xtensa)- a completely diffrent instruction set. So we need to convert the MAC machine code to Xtensa machine code that where this command is used.<cross-compiler>.

Simple words,
1. Create a specialized Python virtual environment.
2. Download the standard xtensa-esp32-elf cross-compiler.
3. Skip downloading the toolchains for other chips (like the S2, S3, or C3). [1] (https://github.com/espressif/esp-idf/blob/master/install.sh)

- alias get_idf='. $HOME/esp/esp-idf/export.sh'
- get_idf
- echo $IDF_PATH    : shows the source path "$" of where our esp-idf path file is stored
- idf.py --version  : checks the version of idf.py file

cd ~/esp
cp -r $IDF_PATH/examples/get-started/hello_world . : copies the exact file out of the mentioned directory
cd hello_world 
idf.py set-target esp32 : tells the build system what exact microchip we gonna work... (32)
idf.py build : to start the build

why idf.py? it is the command-line command centre for entire esp-idf ecosystem.

## END OF M3 

- idf.py -p <port-location> flash monitor
  - -p to set port
  - flash : flashes the firmware into the board's flash memory.
  - monitor : opens a serial terminal at 115200 baud and shows whatever the chip prints.

## Final Takeaways:
- **Why python .12 not .13 versions?** : smaller packages in .13 new version lags but .12 gives a full coverage.
- **Why use two terminal** : we have 3 space local machine, venv and esp-now's local storage. so each 'active' cmd 
                             shoves one-another.

## MODULE 04 : GOAL - THE FIRST CSI
- git clone https://github.com/espressif/esp-csi.git : gives the project and api to work with esp32 csi(channel state information).

Flash pair (To make pipline of sending and reciveing)
1. For sender
- cd ~/esp/esp-csi/examples/get-started/csi_send
- idf.py set-target esp32
- idf.py -p <port_number> flash
2. For reciever
- cd ~/esp/esp-csi/examples/get-started/csi_recv
- idf.py set-target esp32
- idf.py -p <port_number> flash

Monitor the CSI protocol (THE CSI IS TRANSMITTED FROM SENDER TO RECIEVER)
- idf.py -p <recv_port_number> monitor

O/P : 
CSI_DATA,80756,1a:00:00:00:00:00,-7,11,1,0,1,1,1,0,0,0,0,-96,0,11,2,226907860,0,47,1,384,1,"[47,-16,2,0,0,0,0,0,0,0,1,-9,6,-36,7,-38,8,-40,10,-39,10,-37,12,-36,15,-36,15,-36,10,-35,3,-36,-2,-40,-3,-42,-4,-41,-2,-39,2,-38,2,-39,1,-39,2,-37,3,-37,7,-38,9,-38,7,-36,-1,-34,-9,-37,-11,-40,-9,-42,-3,-22,-4,-44,-5,-46,-7,-48,-8,-45,-5,-45,-1,-48,1,-47,1,-46,-2,-47,-10,-46,-17,-46,-19,-45,-17,-45,-11,-48,-7,-50,-7,-53,-8,-53,-4,-52,4,-53,9,-52,9,-51,7,-50,-1,-52,-7,-55,-4,-53,0,-52,0,-13,0,0,0,0,0,0,0,0,1,0,6,3,35,17,37,16,37,15,37,14,22,-7,22,-8,22,-7,22,-8,20,-8,20,-8,20,-11,21,-12,20,-11,19,-10,19,-9,18,-8,18,-8,19,-10,19,-11,20,-12,20,-13,21,-12,20,-12,19,-14,19,-15,19,-15,19,-14,17,-13,16,-14,16,-15,41,-1,17,-16,16,-18,16,-20,17,-20,18,-20,18,-22,19,-22,20,-23,20,-23,19,-21,17,-19,17,-17,19,-18,21,-20,22,-21,23,-21,22,-21,23,-22,25,-23,26,-24,26,-23,26,-20,23,-17,22,-16,23,-15,25,-14,9,-3,2,0,-1,-1,-2,-1,-1,-1,0,0,0,0,-1,-1,-1,-1,-1,-1,0,4,0,20,0,23,-2,24,-2,24,-3,22,-2,22,-1,25,-1,26,-4,24,-5,23,-5,21,-7,20,-8,20,-7,21,-5,21,-6,22,-10,24,-11,23,-9,23,-8,23,-7,23,-7,23,-8,22,-8,20,-7,18,-6,17,-30,17,-6,18,-5,19,-4,21,-5,21,-5,22,-4,23,-4,23,-5,24,-4,24,-3,21,-1,18,-2,17,-2,19,-1,21,-1,22,-1,22,-1,22,1,21,3,23,4,23,5,25,4,23,3,19,3,17,3,18,3,20,-22,33,-22,35,-20,36,-19,38,-3,5]"

## MODULE 05 : GOAL - THE IMP THINGS IN REPO
 -> refer the docs csi-format.md

## MODULE 06 : GOAL - CREATING THE Capture.py 
refer 
- capture.py
- capture.md
  
