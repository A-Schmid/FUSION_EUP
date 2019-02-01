#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_Button.h"

FusionButton::FusionButton(unsigned int button_pin) : FusionModule()
{
    pin = button_pin;
}

void FusionButton::checkButtonState()
{
    bool buttonDown = digitalRead(pin);

    if(buttonDown == LOW)
    {
        if(wasDown == false)
        {
            wasDown = true;
            sendData("button_state", true);
        }
    }
    else
    {
        if(wasDown == true)
        {
            wasDown = false;
            sendData("button_state", false);
        }
    }
}
