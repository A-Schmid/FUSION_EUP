#!/home/fusion/fusion-env/bin/python3

import sys
import os
from functools import partial
from threading import Thread
import time

def write_to_log(msg):
    with open("/tmp/logfile.txt", "a") as logfile:
        logfile.write("{}\n".format(msg))

import numpy as np

from stream_parser import StreamParser
from stream_parser import DataContainer
from stream_parser import bme280Data

import serial

import json

outpath = '/dev/FUSION/'

ser = serial.Serial()
ser.port = port
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonoff = False
ser.dsrdtr = False

#FIXME: RingBuffer for lost messages and for save messages

try:
    #FIXME: if serial port available open, else use pseudo data
    #FIXME: put ser.read() stuff in try block
    ser.open()
except:
    warnings.warn('Failed to open serial port.')

buf_size = 512
sp = StreamParser(buf_size)
dc = DataContainer()
bme280 = bme280Data()

nodeData = {}

def sp_callback(dc):
    global testData
    
    for d in dc.new_data_for:
        if( type(dc.new_data_for[d]) is bme280Data ):
            nodeData[d] = {}
            bme280 = dc.new_data_for[d]
            
            try:
              os.stat(outpath)
            except:
              os.makedirs(outpath)

            path = outpath + "node{}_in".format(bme280.ni)
            outfile = open(path, "w")
            outfile.write(str(bme280.ni) + "\n")
            outfile.write(str(bme280.heart_beat) + "\n")
            outfile.write(str(bme280.temperature) + "\n")
            outfile.write(str(bme280.pressure) + "\n")
            outfile.write(str(bme280.humidity) + "\n")

sp.parsed_all_callback = sp_callback

def blocking_task():
    bme280 = bme280Data()
    ct = 0
    #FIXME: dynamische Gestaltung
    t = {}
    for i in range(7):
        t[i] = bme280 

    # here read serial
    while True:
        
        #
        # read serial data and hand it to parser (note, that parser is blocking)
        #

        if ( ser.in_waiting ):
           sp.buf( ser.read(ser.in_waiting) )
           print( sp._buf.read( sp._buf.len ) )

        #
        # parse data
        # 

        new_data = sp.parse()

        for i in range(7):
            t[i].set_nan()

        for d in new_data:
            if ( type( new_data[d] ) is bme280Data ):
                bme280 = new_data[d]
                t[d] = bme280
             
        for d in t: 
            test = t[d]
            testData = test.heart_beat

        time.sleep(1)
        ct += 1

thread = Thread(target=blocking_task)
thread.start()
