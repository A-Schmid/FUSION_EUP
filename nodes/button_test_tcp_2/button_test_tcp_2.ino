#define DEBUG 1
#include "FUSION_GPIO.h"

#define NODE_ID 43

FusionGPIO gpio(NODE_ID);

uint8_t buttonPin = 0;

void setup()
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  gpio.initialize();
  sendHandshake(NODE_ID);
}

void loop()
{
  Serial.println("loop");
  //gpio.sendData(gpio.dRead(buttonPin));

  gpio.update();

  delay(50);
}
