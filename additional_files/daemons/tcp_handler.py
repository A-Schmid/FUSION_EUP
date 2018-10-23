import socket
import sys
import os
import time

uds_path = "/dev/FUSION"
uds_addr = "{}/node1".format(uds_path)
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

uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
uds_sock.bind(uds_addr)
uds_sock.listen(1)

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



