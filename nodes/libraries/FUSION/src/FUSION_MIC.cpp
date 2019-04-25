#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_MIC.h"

FusionMic::FusionMic(unsigned int sensor_pin) : FusionModule()
{
    pin = sensor_pin;
    pinMode(pin, INPUT);
}

void FusionMic::update()
{
  int volume_intensity = analogRead(pin);
  sendData(volume_intensity, "audio_signal");
}
