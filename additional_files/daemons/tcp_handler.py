import socket
import sys
import os
import time

uds_path = "/tmp/FUSION"
ip_addr = "192.168.4.1"
port_udp = 5005
port_tcp = 5006

try:
    os.stat(uds_path)
except:
    os.makedirs(uds_path)

try:
    os.unlink(uds_addr)
except OSError:
    if os.path.exists(uds_addr):
        raise


tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcp_sock.setblocking(0)
#tcp_sock.settimeout(0.1)
tcp_sock.bind((ip_addr, port_tcp))
tcp_sock.listen(1)

class Node():
    self.tcp_sock = None
    self.uds_sock = None
    self.ni = 0
    self.initialized = False
    self.tcp_queue = []
    self.udp_queue = []

    self.__init__(ni, tcpsock, udssock):
        self.ni = ni
        self.tcp_sock = tcpsock
        self.uds_sock = udssock
        self.initialized = True

    def __handle_communication(self):
        pass

connected_clients = []

def HandleClients():
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
            uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            uds_sock.bind(uds_addr)
            uds_sock.listen(1)
        except:
            print("uds sock connection failed")
            continue

        client_object = Node(client_ni, client, uds_sock)
        connected_clients.append(client_object)
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


