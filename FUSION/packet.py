import struct
from .config import *

class Packet():
    def __init__(self, msg_type = 2, msg_id = 0, node_id = 0, data = []):
        self.msg_type = msg_type
        self.msg_id = 0
        self.node_id = node_id
        self.data = data
        self.data_length = len(data)
        self.checksum = self.generate_checksum()
        pass
    
    def generate_checksum(self): # TODO
        checksum = 0
        return checksum

    def serialize(self): # TODO
        serialized = struct.pack("<BBBBB{}BH".format(self.data_length), 0xAA, self.msg_type, self.msg_id, self.node_id, self.data_length, *self.data, self.checksum) # TODO
        return serialized

    @classmethod
    def deserialize(cls, data):
        msg_type = data[INDEX_MSG_TYPE]
        msg_id = data[INDEX_MSG_ID]
        node_id = data[INDEX_NI]
        data_length = data[INDEX_NMB_DATA]
        msg_data = data[INDEX_DATA : (INDEX_DATA + data_length)]
        # TODO something something checksum
        return cls(msg_type, msg_id, node_id, msg_data)
