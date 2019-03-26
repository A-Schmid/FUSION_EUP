#define DEBUG 1
#include "FUSION_PIN.h"

FusionPin red = FusionPin(D0);
FusionPin yellow = FusionPin(D6);
FusionPin green = FusionPin(D8);

void setup()
{
    Serial.begin(9600);

    //red = FusionPin(D0);
    //yellow = FusionPin(D6);
    //green = FusionPin(D8);

    delay(3000);
    red.initialize(OUTPUT);
    Serial.println("red");
    yellow.initialize(OUTPUT);
    Serial.println("yellow");
    //green.initialize(OUTPUT);
}

void loop()
{
    red.update(); 
    //yellow.update(); 
    //green.update(); 

    delay(update_time);
}
