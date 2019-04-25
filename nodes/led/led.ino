#include "FUSION_LED.h"

FusionLed led = FusionLed(D0);

void setup()
{
    Serial.begin(9600);
    led.initialize();
}

void loop()
{
    led.update(); 

    delay(update_time);
}
