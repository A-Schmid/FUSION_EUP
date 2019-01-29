#ifndef FUSION_MQTT_H
#define FUSION_MQTT_H

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "FUSION_UTILS.h"

#include <stdlib.h>
#include "Adafruit_Sensor.h"
#include <DHT.h>
#include <Wire.h>
#include <map>

class FusionMQTT
{
    public:
        FusionMQTT();
        char* topic_network;
        char* topic_location;
        char* topic_name;
        void init();
        void send(char* dataType, uint16_t data);
        void send(char* dataType, uint8_t* data, unsigned int length);
        void send(char* dataType, const char* data);
        void update();
        void registerCallback(void (*callback_function)(byte*, int), char* topic);
        void callback(char* topic, byte* payload, unsigned int length);

    private:
        WiFiClient wifiClient;
        PubSubClient mqttClient;
        //char* wifi_ssid;
        //char* wifi_password;
        //char* mqtt_server;
        //unsigned int mqtt_port;
        std::map<std::string, std::vector<void (*)(byte*, int)>> callbacks;
};

#endif
