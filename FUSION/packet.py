class Packet():
    def __init__(self, data_string):
        self.raw_data = data_string
        try:
            self.deserialize()
        except:
            #this is not how a checksum works, but better than nothing for now
            self.checksum_ok = False
    def getData(self):
        return self.data
    def getRawData(self):
        return self.raw_data
    def deserialize(self):
        self.raw_bytes = list(self.raw_data[0])
        self.ni = self.raw_bytes[3]
        self.heartbeat = self.raw_bytes[1]
        self.data_length = self.raw_bytes[4]
        self.data = self.raw_bytes[5:5 + self.data_length]
        self.checksum = self.raw_bytes[5 + self.data_length:7+self.data_length]
        self.checksum_ok = True
