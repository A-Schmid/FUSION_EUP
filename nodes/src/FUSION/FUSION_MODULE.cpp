#ifndef FUSION_MODULE_CPP
#define FUSION_MODULE_CPP

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_MODULE.h"
#include <stdlib.h>

FusionModule::FusionModule(unsigned int ni)
{
    nodeId = ni;
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
        Serial.println(data[i], HEX);
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
#endif
