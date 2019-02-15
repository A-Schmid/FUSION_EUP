#ifndef FUSION_PIR_H
#define FUSION_PIR_H

#include "FUSION_MODULE.h"

class FusionPir : public FusionModule
{
    public:
        FusionPir(unsigned int sensor_pin);

        unsigned int pin;
        bool isTracked;

        void checkSensorState();
};

#endif
