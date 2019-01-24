import atexit
import threading
import time
import socket
import sys
import select
import paho.mqtt.client as mqtt
from .core import *

class Module():
    def __init__(self, node_id):
        self._uds_path = FUSION_PATH + 'node{}'.format(node_id)
        self.node_id = node_id
        self._callbacks = {}
        self._connected = False
        self.time = 0
        atexit.register(self.onExit)

    def _uds_connect(self):
        self._uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._uds_sock.setblocking(0)
        
    def _wait_for_connection(self):
        # loop?
        while self._connected == False:
            try:
                self._uds_sock.connect(self._uds_path)
                self._connected = True
                print("connection established - node: {}, fd: {}, sockname: {}, peername: {}".format(self.node_id, self._uds_sock.fileno(), self._uds_sock.getsockname(), self._uds_sock.getpeername()))
            except socket.error as msg:
                print("could not connect to UDS: ", msg, self._uds_path) # daemon not running?
                time.sleep(0.1)

    def _start_update_thread(self, arguments=()):
        thread = threading.Thread(target=self._update, args=arguments)
        thread.daemon = True
        thread.start()

    def _sendToUDS(self, packet):
        timeout = 10
        while(True):
            readable, writeable, exceptional = select.select([], [self._uds_sock], [], 0.5)
            if(self._uds_sock in writeable):
                break
            timeout -= 1
            if(timeout <= 0):
                raise Exception("Timeout in sendToUDS")
        self._uds_sock.sendall(packet)

    def _receiveFromUDS(self):
        timeout = 10
        while(True):
            readable, writeable, exceptional = select.select([self._uds_sock], [], [], 0.5)
            if(self._uds_sock in readable):
                break
            timeout -= 1
            if(timeout <= 0):
                raise Exception("Timeout in receiveFromUDS")
        answer = self._uds_sock.recv(1024)
        return answer

    def _update(self):
        pass

    def disconnect(self):
        #TODO
        pass

    def info(self):
        print("module")

    def onExit(self):
        #TODO
        self.disconnect()
        print("exit!", self.node_id)
