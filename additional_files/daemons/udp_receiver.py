import socket
import time
import datetime
import os

ip_addr = "192.168.4.1"
port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip_addr, port))

print("connecting...")

class Packet():
	def __init__(self, data_string):
		raw_data = bytearray()
		raw_data.extend(map(ord, data_string))
		self.ni = raw_data[3]
		self.heartbeat = raw_data[1]
		self.data_length = raw_data[4]
		self.data = raw_data[5:5 + self.data_length]
		self.checksum = raw_data[5 + self.data_length:7+self.data_length]
		self.checksum_ok = True
	def getData(self):
		return self.data

while True:
    data, addr = sock.recvfrom(1024)
    pack = Packet(data)
    
    outpath = '/dev/FUSION/UDP'.replace("\"", "")#.replace("(", "").replace(")", "").replace(" ", "_")
    try:
        os.stat(outpath)
    except:
        os.makedirs(outpath)
    
    outfile = open(outpath + "/node{}".format(pack.ni), "w")
    outfile.write(str(pack.ni) + "\n")
    outfile.write(str(pack.heartbeat) + "\n")
    outfile.write(str(pack.getData()[0]) + "\n")
    outfile.write(str(time.time()) + "\n")
    outfile.close()
    
    time.sleep(0.1)

