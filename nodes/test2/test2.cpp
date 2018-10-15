#include "Arduino.h"

void setup()
{
        pinMode(D4, OUTPUT);
}

void loop()
{
        digitalWrite(D4, HIGH);
        delay(500);
        digitalWrite(D4, LOW);
        delay(500);
}
