#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_Button.h"

FusionButton::FusionButton(unsigned int button_pin) : FusionModule()
{
    pin = button_pin;
    pinMode(pin, INPUT);
}

void FusionButton::update()
{
    bool buttonDown = digitalRead(pin);

    if(buttonDown == LOW)
    {
        if(wasDown == false)
        {
            wasDown = true;
            sendData(true, "button_state");
        }
    }
    else
    {
        if(wasDown == true)
        {
            wasDown = false;
            sendData(false, "button_state");
        }
    }
}
