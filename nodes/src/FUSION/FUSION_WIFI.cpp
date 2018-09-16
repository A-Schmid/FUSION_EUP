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
            if(!tcpClient.connected())
            {
		        tcpClient.stop();

		        if(!tcpClient.connect(ip, tcp_port))
    		    {
	    	    	delay(500);
		        	return false;
	    	    }
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
