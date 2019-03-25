# 1 "/tmp/tmpp1hrwc58"
#include <Arduino.h>
# 1 "/home/fusion/FUSION_EUP/nodes/pio/src/minimal.ino"
#define DEBUG 1
#include "FUSION_MINIMAL.h"





FusionMinimal module;
void setup();
void loop();
#line 10 "/home/fusion/FUSION_EUP/nodes/pio/src/minimal.ino"
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