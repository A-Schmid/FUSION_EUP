class Module():
    def __init__(self, node_id):
        self.__uds_path = '/tmp/FUSION/node{}'.format(node_id)
        self.node_id = node_id

        self.__uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        
        try:
            self.__uds_sock.connect(self.__uds_path)
        except socket.error as msg:
            print("could not connect to UDS: ", msg) # daemon not running?
            sys.exit(1)

        thread = threading.Thread(target=self.__update, args=())
        thread.daemon = True
        thread.start()
    
    def __update(self):
        pass
