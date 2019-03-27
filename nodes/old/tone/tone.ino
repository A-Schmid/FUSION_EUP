#include "FUSION_TONE.h"

#ifndef PIN
    #define PIN 14 // ESP8266 D5
#endif

FusionTone f_tone(PIN);

void setup()
{
    Serial.begin(9600);
    f_tone.initialize();
}

void loop()
{
    f_tone.update();
    delay(update_time);
}
