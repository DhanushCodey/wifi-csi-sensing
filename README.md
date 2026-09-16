# wifi-csi-sensing

Human's presence sensing project withput using speaker, sensor or camera by via CSI(channel state information) in esp32.


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

## Module - 02 - GOAL : (CHECK HARDWARE)

RUN THESE THREE COMMAND :
- source .venv/bin/activate 
- pip install esptool
- pip freeze > requirements.txt


Ask chip What it is : (it get's the detail)
- ls /dev/usbserial.cu*
- esptool.py --port /dev/cu.usbserial-0001 flash_id

## Module 03 - GOAL : (ESP-IDF(Espressif Iot development famework) (INSTALL)
- brew install cmake ninja dsp-utils
- mkdir -p ~/esp && cd ~/esp
- git clone -b release/v5.5 --recursive https://github.com/espressif/esp-idf.git
-

cmake (build sys generator) -   the architect turn our code into blue print
ninja (the builder)         -   takes the blueprint and compile and link the code. Has extreme execution speed
dfu-utils (connecter)       -   cmd line program used to upload and download device firmware via usb

=> C++/C code -> cmake(generate build instruction) -> ninja (compiles code into final .bin file) -> dfu-utils (Flasher the bin to the native usb)

C++ -> Cmake -> Ninja -> dfu-util(packet manager)

- mkdir -p ~/esp && cd ~/esp
- git clone -b release/v5.5 --recursive https://github.com/espressif/esp-idf.git

creating a directory and downloading the core esp-idf framework and its dependent libraries.

cd ~/esp/esp-idf
./install.sh esp32

esp32 runs (Xtensa)- a completely diffrent instruction set. So we need to convert the MAC machine code to Xtensa machine code that where this command is used.<cross-compiler>.

Simple words,
1. Create a specialized Python virtual environment.
2. Download the standard xtensa-esp32-elf cross-compiler.
3. Skip downloading the toolchains for other chips (like the S2, S3, or C3). [1] (https://github.com/espressif/esp-idf/blob/master/install.sh)


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
  : -p to set port, flash : flashes the firmware into the board's flash memory.
  : monitor : opens a serial terminal at 115200 baud and shows whatever the chip prints.