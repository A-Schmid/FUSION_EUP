#define DEBUG 1
#include "FUSION_MQTT.h"

FusionMQTT mqtt;

void switchLed1(char* topic, byte* payload, int length)
{
    digitalWrite(16, payload[0]);
}

void switchLed2(char* topic, byte* payload, int length)
{
    digitalWrite(12, payload[0]);
}

void switchLed3(char* topic, byte* payload, int length)
{
    digitalWrite(15, payload[0]);
}

void setup()
{
    Serial.begin(9600);
    pinMode(16, OUTPUT);
    pinMode(12, OUTPUT);
    pinMode(15, OUTPUT);

    mqtt = FusionMQTT();
    mqtt.init();

    delay(3000);

    mqtt.registerCallback(&switchLed1, "FUSION/1104/led/led1");
    mqtt.registerCallback(&switchLed2, "FUSION/1104/led/led2");
    mqtt.registerCallback(&switchLed3, "FUSION/1104/led/led3");
}

void loop()
{
    Serial.println("loop");
    mqtt.update(); 
    delay(update_time);
}
