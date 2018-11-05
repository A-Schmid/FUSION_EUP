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
#tcp_sock.setblocking(0)
#tcp_sock.settimeout(0.1)
tcp_sock.bind((ip_addr, port_tcp))
tcp_sock.listen(1)

class Node():
    tcp_sock = None
    uds_sock = None
    ni = 0
    initialized = False
    tcp_queue = []
    uds_queue = []

    def __init__(self, ni, tcpsock, udssock):
        print("init...")
        self.ni = ni
        self.tcp_sock = tcpsock
        self.uds_sock = udssock
        self.initialized = True
        self.active = False

    def start(self):
        print("starting...")
        communicationHandler = Thread(target=self.__handle_communication)
        communicationHandler.start()

    def disconnect(self):
        #TODO
        self.active = False
        self.tcp_sock.close()
        self.uds_sock.close()
        connected_clients.remove(self)
        pass

    def __handle_communication(self):
        print("handle comm...")
        while(self.active):
            readable, writeable, exceptional = select.select([self.uds_sock, self.tcp_sock], [self.uds_sock, self.tcp_sock], [], 0.1)
            """
            if(len(readable) > 0):
                print("avail")
            if(self.tcp_sock in readable):
                print("tcp")
            if(self.uds_sock in readable):
                print("uds")
                """
            #print(len(readable))
            #print(self.tcp_sock in readable)
            #time.sleep(1)
            #continue
            #print(self.uds_sock in readable, self.tcp_sock in readable)

            # read uds
            # TODO handle disconnect
            if(self.uds_sock in readable):
                try:
                    data = self.uds_sock.recv(1024)
                    if(len(data) == 0):
                        self.disconnect()
                        #TODO handle DC
                        print("disconnected uds")
                    self.tcp_queue.append(data)
                except OSError as msg:
                    print("couldn't read uds sock", msg)
            # read tcp

            if(self.tcp_sock in readable):
                try:
                    data = self.tcp_sock.recv(1024)
                    self.uds_queue.append(data)
                except:
                    print("couldn't read tcp sock")

            #print(self.uds_sock in writeable, self.tcp_sock in writeable, len(self.uds_queue), len(self.tcp_queue))
            # write uds

            if(len(self.uds_queue) > 0 and self.uds_sock in writeable):
                #print("write uds")
                for data in self.uds_queue:
                    try:
                        # send length?
                        self.uds_sock.sendall(data)
                        self.uds_queue.remove(data)
                    except:
                        print("couldn't send to uds sock")

            # write tcp
            if(len(self.tcp_queue) > 0 and self.tcp_sock in writeable):
                #print("write tcp")
                for data in self.tcp_queue:
                    try:
                        # send length?
                        self.tcp_sock.sendall(data)
                        self.tcp_queue.remove(data)
                    except:
                        print("couldn't send to tcp sock")
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
        #clientList[client_ni] = {"ni" : client_ni, "client" : client, "addr" : addr}

        uds_addr = "{}/node{}".format(uds_path, client_ni)
        try:
            os.unlink(uds_addr)
        except OSError:
            if os.path.exists(uds_addr):
                raise

        # maybe this has to go inside a loop, in case the node connects when the notebook is not running yet?
        try:
            uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            uds_sock.bind(uds_addr)
            uds_sock.listen(1)
        except:
            print("uds sock connection failed")
            continue

        uds_conn, uds_addr  = uds_sock.accept()
        uds_conn.setblocking(0)

        client_object = Node(client_ni, client, uds_conn)
        connected_clients.append(client_object)
        client_object.active = True
        client_object.start()
        time.sleep(0.1)


clientHandler = Thread(target=HandleClients)
clientHandler.start()

"""
while True:
    inputs = [tcp_sock]
    readable, writeable, exceptional = select.select([tcp_sock], [], [], 0)
    for sock in readable:
        if sock.is_server():
            connection, address = sock.accept()
            client_ni = 0
            try:
                client_ni = connection.recvfrom(1024)
            except:
                continue
            client_ni = int.from_bytes(client_ni[0], "big")
            print("client found: ", client_ni)
            connection.send(bytes([0x01])
            connection.setblocking(0)

            connected_clients.append(Node(client_ni, connection, 
"""
"""
cli_list = []

while True:
    while(len(cli_list) < 1):
        cli, addr = uds_sock.accept()
        cli_list.append(cli)

    while True:
        try:
            for cli in cli_list:
                try:
                    cli.send(b'0xAA')
                except:
                    cli_list.remove(cli)
                    raise
            time.sleep(1)
        except:
            break
"""


