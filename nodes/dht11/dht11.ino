#define DEBUG 1
#include "FUSION_DHT11.h"

uint8_t sensorPin = D4;

FusionDHT11 sensor(NODE_ID, sensorPin);

void setup()
{
    Serial.begin(9600);
    sensor.initialize();
}

void loop()
{
    sensor.update();
    delay(5000);
}
