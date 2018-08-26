import socket
import time
import datetime
import os
import sys
import struct

ip_addr = "192.168.4.1"
port = 5006

fusion_path = "/dev/FUSION"

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.bind((ip_addr, port))
sock_tcp.listen(1)
client, addr = sock_tcp.accept()

counter = 0

class Packet():
    def __init__(self, data_string):
        self.raw_data = data_string
        self.deserialize()
    def getData(self):
        return self.data
    def getRawData(self):
        return self.raw_data
    def deserialize(self):
        self.raw_bytes = list(self.raw_data[0])
        self.ni = self.raw_bytes[3]
        self.heartbeat = self.raw_bytes[1]
        self.data_length = self.raw_bytes[4]
        self.data = self.raw_bytes[5:5 + self.data_length]
        self.checksum = self.raw_bytes[5 + self.data_length:7+self.data_length]
        self.checksum_ok = True

while True:
    # WIP!
    print(counter)
    FRAME_BEGIN = 0xAA
    FRAME_ID = 0
    MSG_ID = 0
    NI = 0
    NMB_DATA = 1
    DATA = counter % 2
    CHECKSUM = 0x0000
    packet = struct.pack("<BBBBBBH", FRAME_BEGIN, FRAME_ID, MSG_ID, NI, NMB_DATA, DATA, CHECKSUM)
    client.sendall(packet)
    counter += 1
    
    time.sleep(1)
