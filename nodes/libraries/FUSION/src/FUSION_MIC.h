#ifndef FUSION_MIC_H
#define FUSION_MIC_H

#include "FUSION_MODULE.h"

class FusionMic : public FusionModule
{
    public:
        FusionMic(unsigned int sensor_pin);
        unsigned int pin;
        void update();
};

#endif
