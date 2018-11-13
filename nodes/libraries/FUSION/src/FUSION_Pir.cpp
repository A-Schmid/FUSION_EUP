#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_Pir.h"

FusionPir::FusionPir(unsigned int sensor_pin, unsigned int ni) : FusionModule(ni)
{
    pin = sensor_pin;
    wait_time = 50;
}

void FusionPir::checkSensorState()
{
    bool motion = digitalRead(pin);
    Serial.println(motion == HIGH);

    if(motion == HIGH)
    {
        if(isTracked == false)
        {
            Serial.println("enter");
            isTracked = true;
            sendData(true);
        }
    }
    else
    {
        if(isTracked == true)
        {
            Serial.println("leave");
            isTracked = false;
            sendData(false);
        }
    }
}
