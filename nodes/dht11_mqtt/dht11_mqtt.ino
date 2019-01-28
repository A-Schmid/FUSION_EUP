#define DEBUG 1
#include "FUSION_MQTT.h"

uint8_t sensorPin = D4;

DHT* sensor;
FusionMQTT mqtt;

void setup()
{
    Serial.begin(9600);
    sensor = new DHT(sensorPin, 11, 6);
    sensor->begin();
    mqtt = FusionMQTT();
    mqtt.init();
}

void loop()
{
    uint8_t humi = sensor->readHumidity();
    uint8_t temp = sensor->readTemperature();
    mqtt.send("temperature", &temp, 1);
    mqtt.send("humidity", &humi, 1);
    delay(update_time);
}
