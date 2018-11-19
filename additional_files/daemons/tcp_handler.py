import socket
import sys
import os
import time
import select
from threading import Thread

uds_path = "/tmp/FUSION"
ip_addr = "192.168.4.1"
port_udp = 5005
port_tcp = 5006

try:
    os.stat(uds_path)
except:
    os.makedirs(uds_path)

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((ip_addr, port_tcp))
tcp_sock.listen(1)

class Node():
    tcp_sock = None
    uds_sock = None
    ni = 0
    initialized = False
    tcp_queue = []
    uds_queue = []

    def __init__(self, ni, tcpsock):
        print("init...")
        self.ni = ni
        self.tcp_sock = tcpsock
        self.initialized = True
        self.active = False

        connectionHandler = Thread(target=self.__connect_uds)
        connectionHandler.start()

    def start(self):
        print("{} - starting...".format(self.ni))
        communicationHandler = Thread(target=self.__handle_communication)
        communicationHandler.start()

    def __connect_uds(self):
        print("{} - connecting uds...".format(self.ni))
        uds_addr = "{}/node{}".format(uds_path, self.ni)
        try:
            os.unlink(uds_addr)
        except OSError:
            if os.path.exists(uds_addr):
                raise

        # maybe this has to go inside a loop, in case the node connects when the notebook is not running yet?
        print("{} - trying to connect uds...".format(self.ni))
        try:
            uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            uds_sock.bind(uds_addr)
            uds_sock.listen(1)
        except:
            print("uds sock connection failed")
        time.sleep(0.1)

        self.uds_sock, self.uds_addr = uds_sock.accept()
        self.uds_sock.setblocking(0)

        self.active = True
        connected_clients.append(self)
        self.start()

    def disconnect(self):
        #TODO
        self.active = False
        self.tcp_sock.close()
        self.uds_sock.close()
        connected_clients.remove(self)
        pass

    def __handle_communication(self):
        print("{} - handle comm...".format(self.ni))
        while(self.active):
            readable, writeable, exceptional = select.select([self.uds_sock, self.tcp_sock], [self.uds_sock, self.tcp_sock], [], 0.5) # 0.1

            # read uds
            # TODO handle disconnect
            if(self.uds_sock in readable):
                try:
                    data = self.uds_sock.recv(1024)
                    if(len(data) == 0):
                        self.disconnect()
                        #TODO handle DC
                        print("{} - disconnected uds".format(self.ni))
                    self.tcp_queue.append(data)
                except OSError as msg:
                    print("{} - couldn't read uds sock".format(self.ni), msg)
            # read tcp

            if(self.tcp_sock in readable):
                try:
                    data = self.tcp_sock.recv(1024)
                    self.uds_queue.append(data)
                except:
                    print("{} - couldn't read tcp sock".format(self.ni))

            # write uds

            if(len(self.uds_queue) > 0 and self.uds_sock in writeable):
                #print("write uds")
                for data in self.uds_queue:
                    try:
                        # send length?
                        self.uds_sock.sendall(data)
                        self.uds_queue.remove(data)
                    except:
                        print("{} - couldn't send to uds sock".format(self.ni))

            # write tcp
            if(len(self.tcp_queue) > 0 and self.tcp_sock in writeable):
                #print("write tcp")
                for data in self.tcp_queue:
                    try:
                        # send length?
                        self.tcp_sock.sendall(data)
                        self.tcp_queue.remove(data)
                    except:
                        print("{} - couldn't send to tcp sock".format(self.ni))
            time.sleep(0.1)
        print("shutting down client ", self.ni)

connected_clients = []

def HandleClients():
    print("handle clients...")
    while True:
        # TODO: security
        try:
            client, addr = tcp_sock.accept()
            client_ni = client.recvfrom(1024) # data format?  
        except socket.error:
            print("tcp socket error")
            continue
        except socket.timeout:
            print("tcp socket timeout")
            continue

        client_ni = int.from_bytes(client_ni[0], "big")
        print("client found ", client_ni)
        client.send(bytes([0x01]))
        client.setblocking(0)

        client_object = Node(client_ni, client)
        time.sleep(0.1)


clientHandler = Thread(target=HandleClients)
clientHandler.start()
