#ifndef FUSION_TONE_H
#define FUSION_TONE_H

#include "FUSION_MODULE.h"

class FusionTone : public FusionModule
{
    public:
        FusionTone(unsigned int p_pin);

        unsigned int pin;

        void update();
    private:
        void playNote(unsigned int frequency, unsigned long duration);
};
#endif
