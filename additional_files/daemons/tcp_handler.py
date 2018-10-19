import socket
import time
import datetime
import os
import sys
import struct
import select
from threading import Thread

ip_addr = "192.168.4.1"
port = 5006

fusion_path = "/dev/FUSION"

try:
    os.stat(fusion_path)
except:
    os.makedirs(fusion_path)

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.setblocking(0)
sock_tcp.settimeout(0.1)
sock_tcp.bind((ip_addr, port))
sock_tcp.listen(1)

clientList = {}

class Packet():
    def __init__(self, data_string):
        self.raw_data = data_string
        try:
            self.deserialize()
        except:
            #this is not how a checksum works, but better than nothing for now
            self.checksum_ok = False
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


def SendData_TCP(nodeId, data):
    data_og = data
    data = bytes(data)
    length = len(data)
    try:
        addr = clientList[nodeId]["addr"]
        client = clientList[nodeId]["client"]
    except:
        print("unknown node")
        return

    #print(client)
    print("sending data to", nodeId)
    print("data: ", data)

    header = length
    client.sendall(bytes([header]))
    print("header: ", header)
    ack = client.recvfrom(1024)
    print("ack: ", ack)

    # WIP!
    FRAME_BEGIN = 0xAA
    FRAME_ID = 0
    MSG_ID = 0
    NI = 0
    NMB_DATA = length
    DATA = data 
    CHECKSUM = 0x0405
    #packet = struct.pack("<BBBBB{}BH".format(NMB_DATA), FRAME_BEGIN, FRAME_ID, MSG_ID, NI, NMB_DATA, DATA, CHECKSUM)
    packet = struct.pack("<BBBBB{}BH".format(NMB_DATA), FRAME_BEGIN, 2, 3, NI, NMB_DATA, *DATA, CHECKSUM)
    print("packet: ", packet)
    client.sendall(packet)

def tcp_receive(client):
    print("recv...")
    try:
        data = client.recvfrom(1024)
    except socket.error:
        print("se")
        return
    except socket.timeout:
        print("st")
        return

    print("receiving data...")

    pack = Packet(data)

    if(pack.checksum_ok == False):
        return

    fifo_path = fusion_path + "/node{}_in".format(pack.ni)

    outfile = open(fifo_path, "w")
    outfile.write(str(pack.ni) + "\n")
    outfile.write(str(pack.heartbeat) + "\n")

    for d in pack.getData():
        outfile.write(str(d))
    outfile.write("\n")

    outfile.write(str(time.time()) + "\n")
    outfile.close()



def HandleClients():
    while True:
        # TODO: security
        try:
            client, addr = sock_tcp.accept()
            client_ni = client.recvfrom(1024) # data format?  
        except socket.error:
            continue
        except socket.timeout:
            continue

        client_ni = int.from_bytes(client_ni[0], "big")
        print("client found ", client_ni)
        client.send(bytes([0x01]))
        clientList[client_ni] = {"ni" : client_ni, "client" : client, "addr" : addr}
        time.sleep(0.1)


clientHandler = Thread(target=HandleClients)
clientHandler.start()

while True:
    #print(clientList)
    for ni, client in clientList.items():
        print(ni)
        inputs = [client["client"]]
        readable, writeable, exceptional = select.select(inputs, [], [])
        if(len(readable > 0)):
            print(client)
            print(client["client"])
            tcp_receive(client["client"])
        print("sending...")
        #ni = client["ni"]
        path = fusion_path + "/node{}_out".format(ni)
        try:
            with open(path, "rb+") as outfile:
                for line in outfile:
                    print(line)
                    data = []
                    for c in line[:-1]: # dont include the line break
                        data.append(int(c))
                    SendData_TCP(ni, data)
                    #print(str.encode(line))
                    #print("---")
                outfile.truncate(0)
        except Exception as e:
            print("something went wrong with client {}: {}".format(ni, e))
    time.sleep(0.1)
