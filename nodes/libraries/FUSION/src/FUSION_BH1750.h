#ifndef FUSION_BH1750_H
#define FUSION_BH1750_H

#include "FUSION_MODULE.h"

class FusionBH1750 : public FusionModule
{
    public:
        unsigned int length;
        int address;

        FusionBH1750(unsigned int ni, int addr);

        void init();

        int read(char* buffer, int len);

        void write();

        void update();
};
#endif

