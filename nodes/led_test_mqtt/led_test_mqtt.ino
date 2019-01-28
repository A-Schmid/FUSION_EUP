#define DEBUG 1
#include "FUSION_MQTT.h"

FusionMQTT mqtt;

void switchLed1(byte* payload, int length)
{
    digitalWrite(16, payload[0]);
}

void switchLed2(byte* payload, int length)
{
    digitalWrite(12, payload[0]);
}

void switchLed3(byte* payload, int length)
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

    mqtt.registerCallback(&switchLed1, "led1");
    mqtt.registerCallback(&switchLed2, "led2");
    mqtt.registerCallback(&switchLed3, "led3");
}

void loop()
{
    mqtt.update(); 
    delay(update_time);
}
