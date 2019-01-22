#ifndef FUSION_MQTT_H
#define FUSION_MQTT_H

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define XSTR(x) #x
#define STR(x) XSTR(x)

class FusionMQTT
{
    public:
        FusionMQTT();
        char* topic_network;
        char* topic_location;
        char* topic_name;
        void init();
        void send(char* dataType, char* data, unsigned int length);

    private:
        WiFiClient wifiClient;
        PubSubClient mqttClient;
        char* wifi_ssid;
        char* wifi_password;
        char* mqtt_server;
        unsigned int mqtt_port;
};

#endif
