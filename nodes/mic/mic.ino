#include "FUSION_MIC.h"

#ifndef PIN
    #define PIN 2 // ESP8266 pin D4
#endif

FusionMic mic = FusionMic(PIN);

void setup()
{
    Serial.begin(9600);
    mic.initialize();
}

void loop()
{
    mic.update();
    delay(update_time);
}
