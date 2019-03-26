import sys
sys.path.append("..")
import socket
import time
import select
import os

path = "/tmp/FUSION/node43"

try:
    os.unlink(path)
except:
    print("unlink")

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(path)
sock.listen(1)
#sock.setblocking(0)
print("connected")
conn, addr = sock.accept()

while True:
    try:
        data = conn.recv(1024)
        print(data)
    except OSError as msg:
        print("error: ", msg)
    time.sleep(1)
