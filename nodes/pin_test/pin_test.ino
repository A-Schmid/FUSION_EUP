#include "FUSION_PIN.h"

FusionPin pin(A0);

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
