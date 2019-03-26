#include "FUSION_Button.h"

// use pin defined by compile parameters
// if it is not defined, use the default pin of wemos d1 mini button shields
#ifndef PIN
    #define PIN 0
#endif

uint8_t buttonPin = PIN;

FusionButton button(buttonPin);

void setup()
{
    button.initialize();
}

void loop()
{
    button.update();
    delay(update_time);
}
