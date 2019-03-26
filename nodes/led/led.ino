#define DEBUG 1
#include "FUSION_PIN.h"

FusionPin red = FusionPin(D0);
FusionPin yellow = FusionPin(D6);
FusionPin green = FusionPin(D8);

void setup()
{
    red.initialize(OUTPUT);
    yellow.initialize(OUTPUT);
    green.initialize(OUTPUT);
}

void loop()
{
    red.update(); 
    yellow.update(); 
    green.update(); 

    delay(update_time);
}
