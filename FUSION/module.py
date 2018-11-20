import threading
import time
import socket
import sys
import select
from .core import *

class Module():
    def __init__(self, node_id):
        self._uds_path = FUSION_PATH + 'node{}'.format(node_id)
        self.node_id = node_id
        self._callbacks = {}
        self._connected = False
        self.time = 0

    def _uds_connect(self):
        self._uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._uds_sock.setblocking(0)
        
    def _wait_for_connection(self):
        # loop?
        while self._connected == False:
            try:
                self._uds_sock.connect(self._uds_path)
                self._connected = True
            except socket.error as msg:
                print("could not connect to UDS: ", msg, self._uds_path) # daemon not running?
                time.sleep(0.1)

    def _start_update_thread(self, arguments=()):
        thread = threading.Thread(target=self._update, args=arguments)
        thread.daemon = True
        thread.start()

    def _update(self):
        pass

    def info(self):
        print("module")
