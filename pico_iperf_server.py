import network
from machine import Pin
#import usocket as socket
import socket
import time
import gc
import micropython

micropython.mem_info()

gc.enable()

led_pin = Pin("LED", Pin.OUT)

AP_SSID = "PICO_SERVER"
AP_PASS = "pico_pass"
PORT    = 12345
REPS    = 1
PACKET_SIZE = 102400

ap = network.WLAN(network.AP_IF)
ap.config(ssid=AP_SSID, password=AP_PASS)
ap.active(True)

while ap.active() == False:
    pass

ip_addr = ap.ifconfig()[0]
print("AP created, IP : {}".format(ip_addr))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
server.bind((ip_addr, PORT))
server.listen(1)
    
conn, addr = server.accept()
print('Got a connection from %s' % str(addr))
led_pin.on()

start_ = time.ticks_us()
for i in range(REPS):
    request = conn.recv(PACKET_SIZE)
    print('', end='.')
    conn.send(b'H'*PACKET_SIZE)
print("Complete")

end_ = time.ticks_us()
time_taken = end_ - start_

if time_taken != 0:
    data_rate = (PACKET_SIZE*REPS*8*2.0)/time_taken
else:
    data_rate = 0

print("Data rate : {} Mbps".format(data_rate))

conn.close()
server.close()
del server, conn, request

gc.collect()
micropython.mem_info()
