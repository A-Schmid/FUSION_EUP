#define DEBUG 1
#include "FUSION_Pir.h"

uint8_t sensorPin = D3;

FusionPir sensor(sensorPin, NODE_ID);

void setup()
{
  pinMode(sensorPin, INPUT);
  Serial.begin(9600);
  sensor.initialize();
}

void loop()
{
  sensor.checkSensorState();

  delay(sensor.wait_time);
}
