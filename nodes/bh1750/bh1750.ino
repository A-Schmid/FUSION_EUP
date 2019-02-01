#define DEBUG 1
#include "FUSION_BH1750.h"

FusionBH1750 sensor;

void setup()
{
    Serial.begin(9600);
    sensor = FusionBH1750();
    sensor.initialize();
}

void loop()
{
    sensor.update();
    delay(update_time);
}
