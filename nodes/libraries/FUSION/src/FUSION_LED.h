#ifndef FUSION_PIN_H
#define FUSION_PIN_H

#include "FUSION_MODULE.h"

class FusionLed : public FusionModule
{
    public:
        FusionLed(unsigned int pin_id);

        void initialize();

        void update();

        unsigned int pin;

    private:
        void mqttCallback(char* topic, byte* payload, int length);
};

#endif
