#define DEBUG 1
#include "FUSION_TONE.h"

FusionTone f_tone(NODE_ID, PIN);

//uint8_t buttonPin = 0;

void setup()
{
    //pinMode(buttonPin, INPUT);
    Serial.begin(9600);
    f_tone.initialize();
}

void loop()
{
    f_tone.update();
    delay(50);
}
