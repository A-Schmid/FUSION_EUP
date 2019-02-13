#define DEBUG 1
#include "FUSION_MQTT.h"

FusionPin red;
FusionPin yellow;
FusionPin green;

void setup()
{
    Serial.begin(9600);

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
