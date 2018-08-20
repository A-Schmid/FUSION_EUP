import socket
import time
import datetime
import os
import sys

ip_addr = "192.168.4.1"
port = 5005

uds_path = "/dev/FUSION/UDP"

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
        #self.raw_bytes = bytearray()
        #self.raw_bytes.extend(self.raw_data) # map(ord, self.raw_data)
        self.raw_bytes = list(self.raw_data)
        self.ni = self.raw_bytes[3]
        self.heartbeat = self.raw_bytes[1]
        self.data_length = self.raw_bytes[4]
        self.data = self.raw_bytes[5:5 + self.data_length]
        self.checksum = self.raw_bytes[5 + self.data_length:7+self.data_length]
        self.checksum_ok = True

while True:
    #print("waiting for packet...")
    data, addr = sock_udp.recvfrom(1024)
    pack = Packet(data)
    
    #print("creating directories")

    try:
        os.stat(uds_path)
    except:
        os.makedirs(uds_path)

    #print("directories created")

    #uds_addr = uds_path + "/node{}_in".format(pack.ni)

    # Make sure the socket does not already exist
    #try:
    #    os.unlink(uds_addr)
    #except OSError:
    #    if os.path.exists(uds_addr):
    #        raise

    # set up uds socket
    #sock_uds = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) # , fileno = sockfile.fileno())

    #try:
    #    print(uds_addr)
    #    sock_uds.connect(uds_addr)
    #    print(sock_uds.fileno())
    #except Exception as e:
    #    print("Socket error: ")
    #    print(e)
    #    sys.exit()
    #print(pack.getRawData())
    #sock_uds.sendall(pack.getRawData())
    #sock_uds.close()

    #print(str(pack.heartbeat))
    
    outfile = open(uds_path + "/node{}_in".format(pack.ni), "w")
    outfile.write(str(pack.ni) + "\n")
    outfile.write(str(pack.heartbeat) + "\n")

    for d in pack.getData():
        outfile.write(str(d))

    outfile.write("\n")
    #outfile.write(str(pack.getData()) + "\n") # getData()[0] ???
    outfile.write(str(time.time()) + "\n")
    outfile.close()

    #print("done")
    
    time.sleep(0.1)
