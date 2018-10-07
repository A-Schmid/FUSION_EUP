#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_MODULE.h"

FusionModule::FusionModule(unsigned int ni)
{
    nodeId = ni;
}

void FusionModule::initialize()
{
    if(initWifi() == true) Serial.println("wifi initialized");
}

void FusionModule::createPacket(char* data, int data_length)
{
	packetLength = data_length + 7;
	int index_checksum = 1 + FRAME_HEAD_LENGTH + data_length;
	packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);
	
	packet[INDEX_FRAME_BEGIN] = FRAME_BEGIN;
	packet[INDEX_FRAME_ID] = 0;
	packet[INDEX_MSG_ID] = 0;
	packet[INDEX_NI] = nodeId;
	packet[INDEX_NMB_DATA] = data_length;
    
    for(int i = 0; i < data_length; i++)
    {
        packet[1 + FRAME_HEAD_LENGTH + i] = data[i];
    }

	packet[index_checksum] = 1;
	packet[index_checksum + 1] = 1;
	packet[index_checksum + 2] = 0; // why?
}

void FusionModule::freePacket()
{
    free(packet);
}

void FusionModule::sendData(char* data, int data_length)
{
    createPacket(data, data_length);
    sendPacket(packet, packetLength);
    freePacket();
}

void FusionModule::sendData(char data)
{
    char data_pack[1] = {data};
    sendData(data_pack, 1);
}

void FusionModule::sendData(int data)
{
    unsigned int length = sizeof(data);
    char data_pack[length];
    for(int i = 0; i < length; i++)
    {
        data_pack[i] = (char) (data >> (i * sizeof(char) * 8));
    }
    sendData(data_pack, length);
}

void FusionModule::sendData(bool data)
{
    unsigned int length = sizeof(data);
    char data_pack[length];
    for(int i = 0; i < length; i++)
    {
        data_pack[i] = (char) (data >> (i * sizeof(char) * 8));
    }
    sendData(data_pack, length);
}
