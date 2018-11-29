#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_WIFI.h"

bool wifi_initialized = false;
bool accepted = false;

WiFiClient tcpClient;
WiFiUDP udpClient;

bool initWifi()
{
    if(wifi_initialized) return true; // check for WL_CONNECTED?

	WiFi.mode(WIFI_STA); 
	WiFi.begin(ssid, pw);
	
	while(WiFi.status() != WL_CONNECTED)
	{
        Serial.print(".");
	    delay(500);
	}
	
    udpClient.begin(udp_port);

    wifi_initialized = true;

    checkConnection();

    return true;
}

bool sendPacket(char* data, unsigned int length)
{
    return sendPacket(data, length, WIFI_MODE_TCP);
}

bool sendPacket(char* data, unsigned int length, unsigned int mode)
{
    int bytesSent;
    switch(mode)
    {
        case WIFI_MODE_TCP:
            while(1)
            {
                if(checkConnection()) break;
            }
    	    bytesSent = tcpClient.write(data, length);
            if(bytesSent != length)
            {
                Serial.print("bytesSent don't match length: ");
                Serial.print(bytesSent);
                Serial.println(length);
            }
            break;
        case WIFI_MODE_UDP:
            udpClient.beginPacket(ip, udp_port);
            udpClient.write(data, length);
            udpClient.endPacket();
            break;
    }
    return true;
}

void sendHandshake(int node_id)
{
    if(accepted) return;
    
    // TODO this is not nice
    char handshakePacket[9];
    handshakePacket[0] = FRAME_BEGIN;
    handshakePacket[1] = MSG_TYPE_HANDSHAKE;
    handshakePacket[2] = 0;
    handshakePacket[3] = node_id;
    handshakePacket[4] = 1;
    handshakePacket[5] = node_id;
    handshakePacket[6] = 1;
    handshakePacket[7] = 1;
    handshakePacket[8] = 0;

    while(1)
    {
        while(!tcpClient.connected()) delay(100);

        Serial.print("sending handshake..."); Serial.println(handshakePacket[5], HEX);
        
        tcpClient.write(handshakePacket, 9);
        
        Serial.println("waiting for ack");
        
        delay(100); //necessary?
        
        char ack = tcpClient.read();
        
        Serial.println(ack, HEX);
        
        if(ack == 1)
        {
            Serial.println("ack: success!");
            accepted = true;
            break;
        }
        delay(500);
    }
}

bool checkConnection()
{
    if(!tcpClient.connected())
    {
        accepted = false;
        tcpClient.stop();

        // was an if before, blocks now
        while(!tcpClient.connect(ip, tcp_port))
	    {
	    	delay(100); // why the delay?
	    }
        sendHandshake(NODE_ID); // maybe this is the magic line of code
    }
    return true;
}

int readPacket(char* data)
{
    Serial.println("rp start");
    while(1)
    {
        if(checkConnection()) break;
    }

    char* packet = (char*) malloc(100);
    int packet_length = 0;
    int buffer = 0;

    while(!tcpClient.available()) delay(10);
    Serial.print("ava: "); Serial.println(tcpClient.available());

    while(1)
    {
        buffer = tcpClient.read();
        if(buffer == -1) break;
        packet[packet_length] = (char) buffer;
        packet_length++;
        Serial.print(buffer, HEX); Serial.print(" ");
    }

    char data_length = packet_length - 7;//packet[INDEX_NMB_DATA];

    Serial.println("");
    Serial.print("pl: "); Serial.println(packet_length);
    Serial.print("dl: "); Serial.println(data_length);

    for(int i = 0; i < 7; i++)
    {
        Serial.print(packet[i], HEX); Serial.print(" ");
    }
    Serial.println("");

    for(int i = 0; i < data_length; i++)
    {
        Serial.print(packet[INDEX_DATA + i], HEX); Serial.print(" ");
        data[i] = packet[INDEX_DATA + i];
    }

    Serial.println("");

    free(packet);

    Serial.println("rp end");
    return data_length;
}
/*
int readPacketOld(char* data)
{
    Serial.println("rp start");
    while(1)
    {
        if(checkConnection()) break;
    }

    int data_length = readLengthPacket();
    if(data_length == 0) return 0;

    Serial.print("datalength: "); Serial.println(data_length);
    char ack[4] = {0xaa, 0x04, 0x00, (char) NODE_ID};
    tcpClient.write(ack, 4);

    int packet_length = data_length + 7;
    char* packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);

    int readLen = tcpClient.readBytes(packet, packet_length);
    if(readLen == 0) return 0;

    for(int i = 0; i < data_length; i++)
    {
        data[i] = packet[INDEX_DATA + i];
        Serial.print(data[i], HEX); Serial.print(" ");
    }

    Serial.println("");

    Serial.println("rp end");
    return data_length;
}*/

int readLengthPacket()
{
    Serial.println("rlp start");
    int length = 2 + FRAME_HEAD_LENGTH + 1 + FRAME_CHECKSUM_LENGTH;
    char* packet = (char*) malloc(length);
    int readLen = 0;
    readLen = tcpClient.readBytes(packet, length);
    if(readLen == 0) return 0;

    // TODO checksum stuff here
    int result = packet[INDEX_DATA];
    //free(packet);
    Serial.println("rlp end");
    return result;
}
