import socket
import time
import datetime
import os
import sys

ip_addr = "192.168.4.1"
port = 5005

uds_path = "/dev/FUSION"

sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_udp.bind((ip_addr, port))

class Packet():
    def __init__(self, data_string):
        self.raw_data = data_string
        self.deserialize()
    def getData(self):
        return self.data
    def getRawData(self):
        return self.raw_data
    def deserialize(self):
        self.raw_bytes = list(self.raw_data)
        self.ni = self.raw_bytes[3]
        self.heartbeat = self.raw_bytes[1]
        self.data_length = self.raw_bytes[4]
        self.data = self.raw_bytes[5:5 + self.data_length]
        self.checksum = self.raw_bytes[5 + self.data_length:7+self.data_length]
        self.checksum_ok = True

while True:
    data, addr = sock_udp.recvfrom(1024)
    pack = Packet(data)
    
    try:
        os.stat(uds_path)
    except:
        os.makedirs(uds_path)

    outfile = open(uds_path + "/node{}_in".format(pack.ni), "w")
    outfile.write(str(pack.ni) + "\n")
    outfile.write(str(pack.heartbeat) + "\n")

    for d in pack.getData():
        outfile.write(str(d))
    outfile.write("\n")
    
    outfile.write(str(time.time()) + "\n")
    outfile.close()
    
    time.sleep(0.1)
