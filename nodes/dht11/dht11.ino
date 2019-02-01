#define DEBUG 1
#include "FUSION_DHT11.h"

uint8_t sensorPin = D4;

FusionDHT11 sensor(sensorPin);

void setup()
{
    Serial.begin(9600);
    //sensor = FusionDHT11(D4);
    sensor.initialize();
}

void loop()
{
    sensor.update();
    delay(update_time);
}
