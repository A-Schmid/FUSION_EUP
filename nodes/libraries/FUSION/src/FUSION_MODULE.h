#ifndef FUSION_MODULE_H
#define FUSION_MODULE_H

#include <stdlib.h>
#include "Adafruit_Sensor.h"
#include <DHT.h>
#include <Wire.h>
#include "FUSION_WIFI.h"
#include "FUSION_MQTT.h"

class FusionModule
{
    public:
        FusionModule();
        FusionMQTT mqtt;
        unsigned int nodeId;
        unsigned int packetLength;
        char* packet;

        void initialize();
        void update();
        void createPacket(char* data, int data_length);
        void createPacket(char* data, int data_length, int type);
        void freePacket();

        void sendData(char data);
        void sendData(int data);
        void sendData(uint8_t data);
        void sendData(uint16_t data);
        void sendData(bool data);
        void sendData(char* data, int length);

        void sendData(const char* topic_data, char* data, int data_length);
        void sendData(const char* topic_data, char data);
        void sendData(const char* topic_data, int data);
        void sendData(const char* topic_data, uint8_t data);
        void sendData(const char* topic_data, uint16_t data);
        void sendData(const char* topic_data, bool data);
        //TODO: all data types
};

#endif // FUSION_MODULE_H
