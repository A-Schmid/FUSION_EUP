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
    // checkConnection has to go first because of reconnect issues
    while(!checkConnection() || !tcpClient.available()) delay(10);

    // random big length for now, maybe use result of available() in the future? 
    char* packet = (char*) malloc(100);
    int packet_length = 0;
    int buffer = 0;

    while(1)
    {
        buffer = tcpClient.read();
        if(buffer == -1) break;
        packet[packet_length] = (char) buffer;
        packet_length++;
        //Serial.print(buffer, HEX); Serial.print(" ");
    }

    char data_length = packet_length - 7;//packet[INDEX_NMB_DATA];

    for(int i = 0; i < data_length; i++)
    {
        //Serial.print(packet[INDEX_DATA + i], HEX); Serial.print(" ");
        data[i] = packet[INDEX_DATA + i];
    }

    //Serial.println("");

    free(packet);

    return data_length;
}

int readLengthPacket()
{
    int length = 2 + FRAME_HEAD_LENGTH + 1 + FRAME_CHECKSUM_LENGTH;
    char* packet = (char*) malloc(length);
    int readLen = 0;
    readLen = tcpClient.readBytes(packet, length);
    if(readLen == 0) return 0;

    // TODO checksum stuff here
    int result = packet[INDEX_DATA];
    //free(packet);
    return result;
}
