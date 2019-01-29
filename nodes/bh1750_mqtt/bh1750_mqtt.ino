#define DEBUG 1
#include "FUSION_BH1750.h"
#include "FUSION_MQTT.h"

FusionBH1750 sensor;
FusionMQTT mqtt;

void setup()
{
    Serial.begin(9600);
    sensor = FusionBH1750();
    sensor.init();
    mqtt = FusionMQTT();
    mqtt.init();
}

void loop()
{
    uint16_t lightIntensity = sensor.readLightIntensity();
    mqtt.send("lightIntensity", lightIntensity);
    delay(update_time);
}
