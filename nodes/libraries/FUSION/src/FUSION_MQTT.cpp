#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif
#include "FUSION_MQTT.h"

FusionMQTT::FusionMQTT()
{
    wifi_ssid = STR(WIFI_SSID);
    wifi_password = STR(WIFI_PASSWORD);
    mqtt_server = STR(MQTT_SERVER);
    mqtt_port = MQTT_PORT;

    topic_network = "FUSION";
    topic_location = "1104";
    topic_name = STR(NODE_NAME);
}

void FusionMQTT::init()
{
    mqttClient = PubSubClient(wifiClient);
    WiFi.begin(wifi_ssid, wifi_password);

    // connect to wifi
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(100);
    }

    mqttClient.setServer(mqtt_server, mqtt_port);

    while (!mqttClient.connected())
    {
        if (!mqttClient.connect("ESP8266Client"))
        {
            delay(100);
        }
    }
}

void FusionMQTT::send(char* dataType, uint8_t* data, unsigned int length)
{
    char topic[128];
    snprintf(topic, 128, "%s/%s/%s/%s", topic_network, topic_location, topic_name, dataType);
    mqttClient.publish(topic, data, length, false);
    mqttClient.loop();
}

void FusionMQTT::send(char* dataType, const char* data)
{
    char topic[128];
    snprintf(topic, 128, "%s/%s/%s/%s", topic_network, topic_location, topic_name, dataType);
    mqttClient.publish(topic, data, false);
    mqttClient.loop();
}

void FusionMQTT::update()
{
    mqttClient.loop();
}
