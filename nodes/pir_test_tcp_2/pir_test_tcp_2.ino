#define DEBUG 1
#include "FUSION_Pir.h"

uint8_t sensorPin = D3;

FusionPir sensor(sensorPin, 43);

void setup()
{
  pinMode(sensorPin, INPUT);
  Serial.begin(9600);
  sensor.initialize();
  sendHandshake(43);
}

void loop()
{
  sensor.checkSensorState();

  delay(sensor.wait_time);
}
