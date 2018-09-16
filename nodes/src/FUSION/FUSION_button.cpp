#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_Button.h"

FusionButton::FusionButton(unsigned int button_pin, unsigned int ni) : FusionModule(ni)
{
    pin = button_pin;
    wait_time = 50;
}

void FusionButton::checkButtonState()
{
    while(1)
    {
        bool buttonDown = digitalRead(pin);

        if(buttonDown == LOW)
        {
            if(wasDown == false)
            {
                wasDown = true;
                sendData(true);
            }
        }
        else
        {
            if(wasDown == true)
            {
                wasDown = false;
                sendData(false);
            }
        }

        delay(wait_time);
    }
}
