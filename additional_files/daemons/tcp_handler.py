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
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((ip_addr, port_tcp))
tcp_sock.listen(1)

class Node():
    def __init__(self, ni, tcpsock):
        print("init...")
        self.ni = ni
        self.tcp_sock = tcpsock
        self.initialized = True
        self.active = False

        self.tcp_queue = []
        self.uds_queue = []

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
            uds_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # doesnt work as expected
            print("bind...")
            uds_sock.bind(uds_addr)
            print("listen...")
            uds_sock.listen(1)
            print("success!")
        except:
            print("uds sock connection failed")
        time.sleep(0.1)

        self.uds_sock, self.uds_addr = uds_sock.accept()
        print("accepted connection - node: {}, fd: {}, sockname: {}, peername: {}".format(self.ni, self.uds_sock.fileno(), self.uds_sock.getsockname(), self.uds_sock.getpeername()))
        self.uds_sock.setblocking(0)

        self.active = True
        connected_clients.append(self)
        self.start()

    def disconnect(self):
        self.active = False
        self.tcp_sock.close()
        self.uds_sock.close()
        connected_clients.remove(self)
        pass

    def __handle_communication(self):
        print("{} - handle comm...".format(self.ni))
        while(self.active):
            readable, writeable, exceptional = select.select([self.uds_sock, self.tcp_sock], [self.uds_sock, self.tcp_sock], [], 0.5) # 0.1

            if(len(exceptional) > 0):
                print("exceptional socket!", exceptional)

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
                    try:
                        if(data[3] != self.ni):
                            print("{} wrong ni: {}".format(self.ni, data[3]))
                    except:
                        print("{} packet without msg_type: {}".format(self.ni, data))
                        raise
                    self.uds_queue.append(data)
                except:
                    print("{} - couldn't read tcp sock".format(self.ni))

            # write uds
            if(len(self.uds_queue) > 0 and self.uds_sock in writeable):
                for data in self.uds_queue:
                    try:
                        # send length?
                        self.uds_sock.sendall(data)
                        self.uds_queue.remove(data)
                    except:
                        msg_ni = -1
                        try:
                            msg_ni = data[3]
                        except:
                            print("{} wrong message format".format(self.ni))
                        print("{} - couldn't send to uds sock, msg_ni = {}, socket = {}, fd = {}".format(self.ni, msg_ni, self.uds_sock.getsockname(), self.uds_sock.fileno()))

            # write tcp
            if(len(self.tcp_queue) > 0 and self.tcp_sock in writeable):
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
            handshake = client.recvfrom(1024) # data format?  
        except socket.error:
            print("tcp socket error")
            continue
        except socket.timeout:
            print("tcp socket timeout")
            continue

        try:
            if(handshake[0][1] != 0):
                print("clienthandler: received non-handshake packet", handshake[0])
                continue
        except:
            print("corrupted handshake packet")
            continue

        client_ni = handshake[0][5] #int.from_bytes(handshake[INDEX_DATA], "big")
        print("client found ", client_ni)
        client.send(bytes([0x01]))
        client.setblocking(0)

        # handle reconnects: overwrite tcp sock of existing client with same ni
        exit_flag = False
        for cli in connected_clients:
            if(cli.ni == client_ni):
                print("reconnect: ", client_ni)
                cli.tcp_sock = client
                exit_flag = True

        if(exit_flag == True):
            continue

        client_object = Node(client_ni, client)
        time.sleep(0.1)


clientHandler = Thread(target=HandleClients)
clientHandler.start()
