#define DEBUG 1
#include "FUSION_MINIMAL.h"

/*
 * minimal working example, just increments a counter and broadcasts it each loop
 */

FusionMinimal module;

void setup()
{
    Serial.begin(9600);
    module.initialize();
}

void loop()
{
    module.update();
    delay(update_time);
}
