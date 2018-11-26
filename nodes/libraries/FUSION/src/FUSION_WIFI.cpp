#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_WIFI.h"

const char* ssid = "FUSION";
const char* pw = "fusionjazz";
const char* ip = "192.168.4.1";
const unsigned int udp_port = 5005;
const unsigned int tcp_port = 5006;

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
        if(!checkConnection()) continue;

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

    //free(handshakePacket);
}

bool checkConnection()
{
    if(!tcpClient.connected())
    {
        tcpClient.stop();

        if(!tcpClient.connect(ip, tcp_port))
	    {
	    	//delay(500); // why the delay?
        	return false;
	    }
        sendHandshake(NODE_ID); // maybe this is the magic line of code
    }
    return true;
}

int readPacket(char* data)
{
    int data_length = readLengthPacket();

    Serial.print("datalength: "); Serial.println(data_length);
    tcpClient.write(0x01);

    int packet_length = data_length + 7;
    char* packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);

    tcpClient.readBytes(packet, packet_length);

    for(int i = 0; i < data_length; i++)
    {
        data[i] = packet[INDEX_DATA + i];
        Serial.print(data[i], HEX); Serial.print(" ");
    }

    Serial.println("");

    return data_length;
}

int readLengthPacket()
{
    int length = 2 + FRAME_HEAD_LENGTH + 1 + FRAME_CHECKSUM_LENGTH;
    char* packet = (char*) malloc(length);
    tcpClient.readBytes(packet, length);
    // TODO checksum stuff here
    int result = packet[INDEX_DATA];
    free(packet);
    return result;
}
