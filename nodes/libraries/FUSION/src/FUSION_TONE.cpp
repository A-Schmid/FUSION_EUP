#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_TONE.h"

FusionTone::FusionTone(unsigned int p_pin) : FusionModule()
{
    pin = p_pin;
}

void FusionTone::update()
{
    FusionModule::update();

    char* data = (char*)malloc(6); 

    int data_length = readPacket(data);

    if(data_length == 0)
    {
        return;
    }

    unsigned int frequency =    (data[0] <<      8)  |
                                 data[1];

    unsigned long duration =   ((data[2] << (3 * 8)) | 
                                (data[3] << (2 * 8)) |
                                (data[4] <<      8)  |
                                 data[5]);

    playNote(frequency, duration);
}

void FusionTone::playNote(unsigned int frequency, unsigned long duration)
{
    if(duration == 0)
    {
        noTone(pin);
    }
    else
    {
        tone(pin, frequency, duration);
    }
}
