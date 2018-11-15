#ifndef FUSION_MODULE_H
#define FUSION_MODULE_H

#define INDEX_FRAME_BEGIN 0
#define INDEX_FRAME_ID 1
#define INDEX_MSG_ID 2
#define INDEX_NI 3
#define INDEX_NMB_DATA 4
#define INDEX_DATA 5

#define FRAME_HEAD_LENGTH 4
#define FRAME_CHECKSUM_LENGTH 2
#define FRAME_BEGIN 0xAA

#include <stdlib.h>
#include "Adafruit_Sensor.h"
#include <DHT.h>
#include "FUSION_WIFI.h"

class FusionModule
{
    public:
        FusionModule(unsigned int ni);
        unsigned int nodeId;
        unsigned int packetLength;
        char* packet;

        void initialize();
        void createPacket(char* data, int data_length);
        void freePacket();
        void sendData(char* data, int data_length);
        void sendData(char data);
        void sendData(int data);
        void sendData(bool data);
        //TODO: all data types
};

#endif // FUSION_MODULE_H
