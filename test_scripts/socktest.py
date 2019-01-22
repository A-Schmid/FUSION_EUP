import sys
sys.path.append("..")
import socket
import time
import select

path = "/tmp/FUSION/node43"
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.setblocking(0)
sock.connect(path)
print("connected")

while True:
    try:
        sock.send(b'asdf')
        print("sent")
    except OSError as msg:
        print("error: ", msg)
    time.sleep(1)
