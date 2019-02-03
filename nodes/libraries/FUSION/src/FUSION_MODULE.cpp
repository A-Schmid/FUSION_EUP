#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_MODULE.h"

// initialize builtin reset function
void(* resetFunc) (void) = 0;

FusionModule::FusionModule()
{
    nodeId = node_id;
}

void FusionModule::initialize()
{
    if(protocol == PROTOCOL_WIFI)
    {
        Serial.println("WIFI MODE");
        if(initWifi() == true) Serial.println("wifi initialized");
    }

    if(protocol == PROTOCOL_MQTT)
    {
        Serial.println("MQTT MODE");
        mqtt.init();
    }
}

void FusionModule::update()
{
    if(protocol == PROTOCOL_MQTT)
    {
        mqtt.update();
    }
}

void FusionModule::createPacket(char* data, int data_length)
{
    createPacket(data, data_length, MSG_TYPE_PACKET);
}

void FusionModule::createPacket(char* data, int data_length, int type)
{
	packetLength = data_length + 7;
	int index_checksum = 1 + FRAME_HEAD_LENGTH + data_length;
	packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);
	
	packet[INDEX_FRAME_BEGIN] = FRAME_BEGIN;
	packet[INDEX_MSG_TYPE] = type;
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

void FusionModule::sendData(bool data)
{
    sendData(TOPIC_UNDEFINED, data);
}

void FusionModule::sendData(int data)
{
    sendData(TOPIC_UNDEFINED, data);
}

void FusionModule::sendData(uint8_t data)
{
    sendData(TOPIC_UNDEFINED, data);
}

void FusionModule::sendData(uint16_t data)
{
    sendData(TOPIC_UNDEFINED, data);
}

void FusionModule::sendData(char data)
{
    sendData(TOPIC_UNDEFINED, data);
}

void FusionModule::sendData(char* data, int length)
{
    sendData(TOPIC_UNDEFINED, data, length);
}

void FusionModule::sendData(const char* topic_data, char* data, int data_length)
{
    if(protocol == PROTOCOL_WIFI)
    {
        createPacket(data, data_length);
        sendPacket(packet, packetLength);
        freePacket();
    }

    if(protocol == PROTOCOL_MQTT)
    {
        mqtt.send(topic_data, data, data_length);
    }
}

void FusionModule::sendData(const char* topic_data, char data)
{
    char data_pack[1] = {data};
    sendData(topic_data, data_pack, 1);
}

void FusionModule::sendData(const char* topic_data, uint8_t data)
{
    char data_pack[1] = {(char) data};
    sendData(topic_data, data_pack, 1);
}

void FusionModule::sendData(const char* topic_data, int data)
{
    unsigned int length = sizeof(data);
    char data_pack[length];
    for(int i = 0; i < length; i++)
    {
        data_pack[i] = (char) (data >> (i * sizeof(char) * 8));
    }
    sendData(topic_data, data_pack, length);
}

void FusionModule::sendData(const char* topic_data, uint16_t data)
{
    unsigned int length = sizeof(uint16_t);
    char data_pack[length];
    for(int i = 0; i < length; i++)
    {
        data_pack[i] = (char) (data >> (i * sizeof(char) * 8));
    }
    sendData(topic_data, data_pack, length);
}

void FusionModule::sendData(const char* topic_data, bool data)
{
    unsigned int length = sizeof(data);
    char data_pack[length];
    for(int i = 0; i < length; i++)
    {
        data_pack[i] = (char) (data >> (i * sizeof(char) * 8));
    }
    sendData(topic_data, data_pack, length);
}
