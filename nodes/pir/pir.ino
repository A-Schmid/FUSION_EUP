#include "FUSION_Pir.h"

#ifndef PIN
    #define PIN D3
#endif

FusionPir sensor(PIN);

void setup()
{
  Serial.begin(9600);
  sensor.initialize();
}

void loop()
{
  sensor.update();
  delay(update_time);
}
