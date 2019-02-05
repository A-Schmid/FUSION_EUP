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
    char topic[TOPIC_MAXLENGTH];
    snprintf(topic, TOPIC_MAXLENGTH, "%s/%s/%s/#", topic_network, topic_location, topic_name);
    mqttClient.subscribe(topic);
    Serial.println("initialized");
}

void FusionMQTT::send(uint16_t data, const char* topic_data)
{
    uint8_t *bytes = (uint8_t*) malloc(2);
    bytes[0] = data >> 8;
    bytes[1] = data & 0xFF;
    send(bytes, 2, topic_data);
}

void FusionMQTT::send(char* data, unsigned int length, const char* topic_data)
{
    char topic[TOPIC_MAXLENGTH];
    snprintf(topic, TOPIC_MAXLENGTH, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);
    mqttClient.publish(topic, (uint8_t*) data, length, false);
    mqttClient.loop();
}

void FusionMQTT::send(uint8_t* data, unsigned int length, const char* topic_data)
{
    char topic[TOPIC_MAXLENGTH];
    snprintf(topic, TOPIC_MAXLENGTH, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);
    mqttClient.publish(topic, data, length, false);
    mqttClient.loop();
}

void FusionMQTT::send(const char* data, const char* topic_data)
{
    char topic[TOPIC_MAXLENGTH];
    snprintf(topic, TOPIC_MAXLENGTH, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);
    mqttClient.publish(topic, data, false);
    mqttClient.loop();
}

void FusionMQTT::update()
{
    mqttClient.loop();
}

void FusionMQTT::callback(char* topic, uint8_t* payload, unsigned int length)
{
    for(std::function<void(char*, uint8_t*, unsigned int)> cb : callbacks[topic])
    {
        cb(topic, payload, length);
    }

    /*
    for(void (*cb)(char*, byte*, int) : callbacks[topic])
    {
        cb(topic, payload, length);
    }
    */
}

// TODO move to std::functions everywhere!
/*
void FusionMQTT::registerCallback(void (*callback_function)(char*, byte*, int), char* topic_data)
{
    char topic[TOPIC_MAXLENGTH];
    snprintf(topic, TOPIC_MAXLENGTH, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);

    callbacks[topic].push_back(callback_function);
}
*/

// TODO test this!
void FusionMQTT::registerCallback(std::function<void(char*, uint8_t*, unsigned int)> callback_function, char* topic_data)
{

    char topic[TOPIC_MAXLENGTH];
    snprintf(topic, TOPIC_MAXLENGTH, "%s/%s/%s/%s", topic_network, topic_location, topic_name, topic_data);

    callbacks[topic].push_back(callback_function);
}
