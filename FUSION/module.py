import threading
import time
import socket
import sys
import select
from .core import *

class Module():
    def __init__(self, node_id):
        self.__uds_path = FUSION_PATH + 'node{}'.format(node_id)
        self.node_id = node_id
        self.__callbacks = {}
        self.__connected = False
        self.time = 0

    def __uds_connect(self):
        self.__uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__uds_sock.setblocking(0)
        
        try:
            self.__uds_sock.connect(self.__uds_path)
        except socket.error as msg:
            print("could not connect to UDS: ", msg) # daemon not running?
            sys.exit(1)
    
    def __wait_for_connection(self):
        # loop?
        while self.__connected == False:
            try:
                self.__uds_sock.connect(self.__uds_path)
                self.__connected = True
            except socket.error as msg:
                print("could not connect to UDS: ", msg, self.__uds_path) # daemon not running?
                time.sleep(0.1)

    def __start_update_thread(self, arguments=()):
        thread = threading.Thread(target=self.__update, args=arguments)
        thread.daemon = True
        thread.start()

    def __update(self):
        pass

    def info(self):
        print("module")
