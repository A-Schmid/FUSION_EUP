#define DEBUG 1
#include "FUSION_DHT11.h"

#ifndef PIN
    #define PIN 2 // ESP8266 pin D4
#endif

uint8_t sensorPin = PIN;

FusionDHT11 sensor(sensorPin);

void setup()
{
    sensor.initialize();
}

void loop()
{
    sensor.update();
    delay(update_time);
}
