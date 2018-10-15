//#include "src/FUSION/FUSION_GPIO.h"
#include "FUSION_GPIO.h"

#define NODE_ID 42

FusionGPIO gpio(NODE_ID);

void setup()
{
  Serial.begin(9600);
  gpio.initialize();

  sendHandshake(NODE_ID);
}

void loop()
{
  gpio.update();

  Serial.println("done");
  
  delay(50);
}
