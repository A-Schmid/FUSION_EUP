#!/usr/bin/env python
#coding=utf-8

import struct
import warnings
from bringbuf.bringbuf import bRingBuf

import numpy as np

# container base class
class BaseMeshData():
    def __init__(self):
        # default values are NaN (to work with bokeh)
        self.ni=np.nan         # node id
        self.msg_id=np.nan     # msg_id
        self.heart_beat=np.nan # heart beat
        #self.inactive_cnt=0         # inactive counter

# container class
class bme280Data(BaseMeshData):
    def __init__(self):
        BaseMeshData.__init__(self)
        # default_values are NaN (to work with bokeh)
        self.temperature=np.nan
        self.pressure=np.nan
        self.humidity=np.nan

    def set_nan(self):
        self.__init__()
    def msg_id():
        return 0xbb
    def is_msg_id(b):
        return (b==0xbb)
    def consistent():
        return (self.msg_id==0xbb)
    def type():
        return True 

class DataContainer():
    def __init__(self):
        self.new_data_for = {} # {node_id:sens_container}
                               # any node_id must be unique in data 
                               # (only current value is of interest) 
                               # sens_container of dissimilar types
                               # depending on what comes in

#FIXME: MAVlink-Integration

class StreamParser():
    """StreamParser is a parser for SimpleStreams
    """
    def __init__(self, buf_size=255):
         self._buf_size = buf_size 
         self._buf = bRingBuf(self._buf_size)
         self._index = 0
         self._dc = DataContainer() # must be initialized empty
         self.parsed_all_callback = None
         #FIXME: implement callback, that is called for each value found during parsing process
         #self.parsed_single_callback = None

    def buf(self, b):
        """blocking processing of data
        """
        self._buf.enqueue( b )
        #self.parse()
  
    def parse(self):
        """parse simple_stream data
        """
        self._dc.new_data_for.clear() # initially clear new data buffer
        while ( self._buf.contains([0xaa]) ):
            # search for next frame begin (first byte is 0xaa) 
            index = self._buf.index([0xaa]) 
            # delete preceding non-frame junk (anything, that is not beginning with 0xaa, cannot be a valid frame) 
            self._buf.dequeue(index) 
            # read head of the supposed frame (which is at the beginning now) 
            frame_head = self._buf.read(4, 0) 
            if (len(frame_head) != 4): 
                warnings.warn('Frame head data is missing at the end. Stop here and try next time.') 
                break 
            # number of bytes available 
            nmb_frame_bytes = frame_head[3]  
            # index of crc is behind data 
            index_crc = nmb_frame_bytes + 4 # plus 4 for frame_id, msg_id, ni, nmb_data 
            # if index_crc is within the outer limit of buffer 
            if ( index_crc < (self._buf.len-1) ): 
                # get checksum bytes 
                crc_bytes =  self._buf.read(2, index_crc)
                # calculate checksum int
                crc = struct.unpack( "H", crc_bytes )[0] 
                # checksum OK? 
                #if ( crc == 0xffff ): 
                if ( self.checksumOK(crc) ): 
                    print('Pseudo Checksum OK. Do further processing.') 
                    msg_id = frame_head[1] 
                    # read and remove frame from buffer 
                    # frame_id, msg_id, ni, nmb_data, data0, ..., datax, crc_hi, crc_lo 
                    frame = self._buf.dequeue(nmb_frame_bytes + 6) 
                    if ( msg_id==0xbb ):
                        bme280_data = struct.unpack('>BBBBBiIIH', frame) 
                        bme280 = bme280Data()
                        bme280.ni = bme280_data[2]
                        bme280.msg_id = bme280_data[3]
                        bme280.heart_beat=bme280_data[4]
                        bme280.temperature=bme280_data[5] / 100.0
                        bme280.pressure=bme280_data[6]
                        bme280.humidity=bme280_data[7] / 1024.0
                        
                        self._dc.new_data_for[bme280.ni]=bme280
        
                        #if msg_id in self._dc.new_data_for:
                        #    self._dc.new_data_for[msg_id].add(node_id)
                        #else:
                        #    self._dc.new_data_for[msg_id] = {node_id} # new set for data
                    #elif ( msg_id==0xba ): 
                    #     frame = buf.dequeue(nmb_frame_bytes + 6)  
                    #     ... 
                    #elif ( msg_id==0xbc ): 
                    #     frame = buf.dequeue(nmb_frame_bytes + 6)  
                    #     ... 
                    else: 
                        warnings.warn('Unknown msg_id. Maybe version of read class and stream object are not compatible.') 
                else: 
                    warnings.warn('no valid data, delete 0xaa, go back to search next 0xaa') 
                  
            else: # lacking crc check bytes 
                warnings.warn('crc is missing at the end. Stop here and try next time.') 
                break

        # only if data is available 
        #FIXME only call if not empty
        if ( bool(self._dc.new_data_for) ):
            # call callback with all parsed data as argument
            print(self._dc.new_data_for)
            if ( not (self.parsed_all_callback == None) ):
                self.parsed_all_callback(self._dc)#new_data(msg_id:[node_id])
        return self._dc.new_data_for

    def checksumOK(self, crc):
        #FIXME: pseudo checksum, todo code real checksum
        return (crc == 0xffff)
