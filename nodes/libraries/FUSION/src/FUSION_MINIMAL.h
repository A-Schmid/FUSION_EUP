#ifndef FUSION_MINIMAL_H
#define FUSION_MINIMAL_H

#include "FUSION_MODULE.h"

class FusionMinimal : public FusionModule
{
    public:
        FusionMinimal();

        char counter;

        void update();
};
#endif

