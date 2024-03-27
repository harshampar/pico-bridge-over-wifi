import network
#import usocket as socket
import socket
from machine import Pin
import time
import gc
import micropython

micropython.mem_info()

gc.enable()

REPS = 1
PACKET_SIZE = 102400
led_pin = Pin("LED", Pin.OUT)

# Connect to your Wi-Fi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("PICO_SERVER", "pico_pass")

# Wait until connected
while not wifi.isconnected():
    pass

led_pin.on()    

# Get the IP address of the Pico
ip_address = wifi.ifconfig()[0]

print("IP address : {}".format(ip_address))

ip_root = ip_address.split('.')
server_ip = ''
for i in ip_root[:-1]:
    server_ip+='{}.'.format(i)

server_ip += '1'

print("Server IP address : {}".format(server_ip))

port = 12345  # Use the same port as defined on the Pico

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, port))

# Send data to the server
start_ = time.ticks_us()
for i in range(REPS):
    client_socket.send(b"H"*PACKET_SIZE)
    print('', end=".")
    response=client_socket.recv(PACKET_SIZE)
print("Complete")

end_ = time.ticks_us()
time_taken = end_ - start_

if time_taken != 0:
    data_rate = (PACKET_SIZE*REPS*8*2.0)/time_taken
else:
    data_rate = 0

print("Data rate : {} Mbps".format(data_rate))

client_socket.close()
del client_socket, response

gc.collect()

micropython.mem_info()
