# Serial connection over Pico WiFi bridge.

This repo deals with opening a serial port over a Pico WiFi bridge.
(Host -> Pico AP -> WiFi -> Pico Client -> Host )

# Setup
- The programs are currently written in Micropython, for ease of development.
    - Will be shifting to using C/C++ SDK soon, as there are only a limited libraries ported in Micropython.
- Load Micropython uf2 into the Pico
    - To load any uf2 into Pico:
        - Press and hold the boot select button(The only button on the Pico).
        - Connect the USB to the laptop.
        - Release the button.
        - The Pico should mount as a drive with 2 files in it.
    - Copy the [file](RPI_PICO_W-20240222-v1.22.2.uf2) into the mounted drive.
        - The file RPI_PICO_W-20240222-v1.22.2.uf2 is added in the repo for ease. 
        - Can be found in Micropython/Raspberry page too.
    - Once copy is complete the drive will unmount itself.
    - The Pico now has a Micropython env running in it, can be used like a python prompt.
    - Remove and plug the Pico USB cable.
- Install [Thonny](https://thonny.org/).
    - General introduction : https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2
    - Main points:
        - Select the Micropython environment.
        - Select /dev/ttyACMx as the board to be programmed.
        - If you need multiple boards to be programmed at once, need to change it in options to allow multiple instances of Thonny.
        - Make sure the two instances interact with the different /dev/ttyACMx ports.
    - Open pico_iperf_server.py in one Thonny instance and pico_iperf_client.py on another instance.
    - Run both the files on different Picos.
    - Notes:
        - There is an option to save the code on to the Pico too, where the python code stays and can be opened and programmed by Thonny. 
            - This way the code will stay inside the Pico, but cannot be used for source control.
            - Better to store the code outside the Pico in the laptop and program it every time.
  
# Explanation
- pico_iperf_server.py
    - Contains code to start AP in the Pico and start a socket in the default server address.
- pico_iperf_client.py
    - Contains code to connect to the AP created by the pico_iperf_server.py and then connect to the socket created by the server code. 
- Once the socket is connected, data of size 102400 is sent back and forth over the socket and time of flight is measured.
    - The data rate is calculated for the same.
- Got data rates around 15-17 Mbps this way.
- Any byte data can be replaced in place of the data sent.

# Notes
- The Pico only has around ~240 kB of memory. And some of it is even taken up by the Micropython interpretor. So I am printing the available memory before and after the test. I am also calling garbage collector to make sure all memory is released. This may not be the best way but works as of now as there is nothing heavy in the code. 

