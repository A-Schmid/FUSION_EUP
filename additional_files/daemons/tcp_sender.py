import socket
import time
import datetime
import os
import sys
import struct
from threading import Thread

ip_addr = "192.168.4.1"
port = 5008

fusion_path = "/dev/FUSION"

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.bind((ip_addr, port))
sock_tcp.listen(1)

counter = 0
clientList = {}

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

def SendData_TCP(nodeId, data):
    data_og = data
    data = bytes([data])
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
    DATA = data_og 
    CHECKSUM = 0x0405
    #packet = struct.pack("<BBBBB{}BH".format(NMB_DATA), FRAME_BEGIN, FRAME_ID, MSG_ID, NI, NMB_DATA, DATA, CHECKSUM)
    packet = struct.pack("<BBBBB{}BH".format(NMB_DATA), FRAME_BEGIN, 2, 3, NI, NMB_DATA, DATA, CHECKSUM)
    print("packet: ", packet)
    client.sendall(packet)

def HandleClients():
    while True:
        # TODO: security
        client, addr = sock_tcp.accept()
        client_ni = client.recvfrom(1024) # data format?
        client_ni = int.from_bytes(client_ni[0], "big")
        print("client found ", client_ni)
        client.send(bytes([0x01]))
        clientList[client_ni] = {"client" : client, "addr" : addr}
        time.sleep(0.1)

clientHandler = Thread(target=HandleClients)
clientHandler.start()
counter = 1

while True:
    #print(clientList)
    SendData_TCP(42, counter%2)
    counter += 1
    time.sleep(1)

"""
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
    """
