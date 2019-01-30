#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif
#include "FUSION_MQTT.h"

FusionMQTT::FusionMQTT()
{

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

    mqttClient.setCallback(std::bind(&FusionMQTT::callback, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3));

    while (!mqttClient.connected())
    {
        if (!mqttClient.connect("ESP8266Client"))
        {
            delay(100);
        }
    }

    // member variable maybe?
    char topic[128];
    snprintf(topic, 128, "%s/%s/%s/#", topic_network, topic_location, topic_name);
    mqttClient.subscribe(topic);
    Serial.println("initialized");
}

void FusionMQTT::send(const char* topic_data, uint16_t data)
{
    uint8_t *bytes = (uint8_t*) malloc(2);
    bytes[0] = data >> 8;
    bytes[1] = data & 0xFF;
    send(topic_data, bytes, 2);
}

void FusionMQTT::send(const char* topic_data, char* data, unsigned int length)
{
    char topic[128];
    snprintf(topic, 128, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);
    mqttClient.publish(topic, (uint8_t*) data, length, false);
    mqttClient.loop();
}

void FusionMQTT::send(const char* topic_data, uint8_t* data, unsigned int length)
{
    char topic[128];
    snprintf(topic, 128, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);
    mqttClient.publish(topic, data, length, false);
    mqttClient.loop();
}

void FusionMQTT::send(const char* topic_data, const char* data)
{
    char topic[128];
    snprintf(topic, 128, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);
    mqttClient.publish(topic, data, false);
    mqttClient.loop();
}

void FusionMQTT::update()
{
    mqttClient.loop();
}

void FusionMQTT::callback(char* topic, byte* payload, unsigned int length)
{
    for(void (*cb)(byte*, int) : callbacks[topic])
    {
        cb(payload, length);
    }
}

void FusionMQTT::registerCallback(void (*callback_function)(byte*, int), char* topic)
{
    Serial.println(topic);
    callbacks[topic].push_back(callback_function);
}
