#include "FUSION_PIN.h"

FusionPin pin = FusionPin(A0);

void setup()
{
    Serial.begin(9600);
    pin.initialize();
}

void loop()
{
    pin.update();
    delay(update_time);
}
