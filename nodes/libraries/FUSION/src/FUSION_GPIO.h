#ifndef FUSION_GPIO_H
#define FUSION_GPIO_H

#include "FUSION_MODULE.h"

class FusionGPIO : public FusionModule
{
    public:
        FusionGPIO(unsigned int ni);

        void update();
        int parseMessage(char* message);
    private:
        void setDirection(unsigned int pin, unsigned int direction);
        void dWrite(unsigned int pin, unsigned int value);
        void aWrite(unsigned int pin, unsigned int value);
        bool dRead(unsigned int pin);
        unsigned int aRead(unsigned int pin);
};
#endif
