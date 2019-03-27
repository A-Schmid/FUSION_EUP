#define XSTR(x) #x
#define STR(x) XSTR(x)
#include "Arduino.h"

String name = STR(NODE_NAME);

void setup()
{
    Serial.begin(9600); 
    delay(1000);
    Serial.println("starting...");
}

void loop()
{
    //int asdf = 5;
    Serial.println(name);
    delay(1000);
}
