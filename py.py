import time
import socket
import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
addr = ("127.0.0.1", 7777)

#for i in range(10):
#    message = "\1\77"
#    client_socket.sendto(message, addr)

# localhost: 7f 00 00 01
# port 5100: 13 EC
# prepare: 2b - block number, 2b - length
# put: 2b - block number, 4b - offset, 2b - length, [length]b - data
# send: 4b - target address, 2b - target port, 2b - block number, 4b - offset, 2b - length 

data_prepare = "\x10" + "\x00\x00" + "\x00\x01"
data_put1 = "\x20" "\x00\x00" "\x00\x00\x00\x00" "\xf0\x00" "\x00\x00" "\x41\x42"
data_put2 = "\x20" "\x00\x00" "\x00\x00\x00\x00" "\x10\x00" "\x00\x00" "\x43\x44"
data_send = "\x30" "\x01\x00\x00\x7f" "\xec\x13" "\x00\x00" "\x10\x00\x00\x00" "\x00\x01"
data_receive = "\x50" "\x00\x00" "\x00\x00\x00\x00"

#client_socket.sendto(data_send, addr)
#client_socket.sendto(data_put2, addr)
#client_socket.sendto(data_put1, addr)
#client_socket.sendto(data_prepare, addr)
client_socket.sendto(data_receive, addr)
print(client_socket.recvfrom(65565)[0][:10])
#client_socket.sendto("\0", addr)