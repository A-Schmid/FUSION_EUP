#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_MINIMAL.h"

FusionMinimal::FusionMinimal() : FusionModule()
{
    // I told you it's minimal!
}

void FusionMinimal::update()
{
   sendData(counter, "value");
   counter++;
}

