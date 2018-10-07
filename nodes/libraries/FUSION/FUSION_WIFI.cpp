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
    if(wifi_initialized) return true;

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
    switch(mode)
    {
        case WIFI_MODE_TCP:
            while(1)
            {
                if(checkConnection()) break;
            }
    	    tcpClient.write(data, length);
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

    char packet[1];
    packet[0] = (char) node_id;
    
    while(1)
    {
        if(!checkConnection()) continue;

        Serial.print("sending handshake..."); Serial.println(packet[0], HEX);
        
        tcpClient.write(packet, 1);
        
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
        tcpClient.stop();

        if(!tcpClient.connect(ip, tcp_port))
	    {
	    	delay(500);
        	return false;
	    }
    }
    return true;
}


int readPacket(char* data)
{
    int data_length = -1;
    while(data_length == -1)
    {
        data_length = (int) tcpClient.read();
    }
    Serial.print("datalength: "); Serial.println(data_length);
    tcpClient.write(0x01);

    int packet_length = data_length + 7;
    int index_checksum = 1 + FRAME_HEAD_LENGTH + data_length;
    char* packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);

    tcpClient.readBytes(packet, packet_length);

    //*data = (char*) malloc(data_length);
    //memcpy(*data, packet + INDEX_DATA, data_length);
    for(int i = 0; i < data_length; i++)
    {
        data[i] = packet[INDEX_DATA + i];
        Serial.print(data[i], HEX); Serial.print(" ");
    }

    Serial.println("");
    Serial.print("led status: "); Serial.println(packet[FRAME_HEAD_LENGTH+1], HEX);

    return data_length;
}
