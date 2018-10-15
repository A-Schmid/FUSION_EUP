#ifndef FUSION_BUTTON_H
#define FUSION_BUTTON_H

#include "FUSION_MODULE.h"

class FusionButton : public FusionModule
{
    public:
        FusionButton(unsigned int button_pin, unsigned int ni);

        unsigned int pin;
        bool wasDown;
        int wait_time;

        void checkButtonState();
};

#endif
