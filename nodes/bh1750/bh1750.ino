#define DEBUG 1
#include "FUSION_BH1750.h"

FusionBH1750 sensor(NODE_ID, 0x23);

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
