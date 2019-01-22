#define DEBUG 1
#include "FUSION_MODULE.h"
#include "FUSION_MQTT.h"

FusionMQTT mucki;

char data = 0;

void setup()
{
    Serial.begin(9600);
    mucki = FusionMQTT();
    mucki.init();
}

void loop()
{
    data += 1;
    mucki.send("testdata", &data, 1);
    delay(1000);
}
