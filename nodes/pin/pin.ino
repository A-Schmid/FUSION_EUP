#include "FUSION_PIN.h"

FusionPin pin = FusionPin(PIN);

void setup()
{
    Serial.begin(9600);
    pin.initialize();
    pin.setDirection(INPUT);
}

void loop()
{
    pin.update();
    delay(update_time);
}
