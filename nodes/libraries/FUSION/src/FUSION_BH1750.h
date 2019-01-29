#ifndef FUSION_BH1750_H
#define FUSION_BH1750_H

#include "FUSION_UTILS.h"

#ifndef I2C_ADDR
#define I2C_ADDR 0x23
#endif

class FusionBH1750
{
    public:
        unsigned int length;
        int address;

        FusionBH1750();

        void init();

        int read(char* buffer, int len);

        void write();

        void update();

        uint16_t readLightIntensity();
};
#endif

