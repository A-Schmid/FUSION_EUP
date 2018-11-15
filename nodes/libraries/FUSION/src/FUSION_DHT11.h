#ifndef FUSION_DHT11_H
#define FUSION_DHT11_H

#include "FUSION_MODULE.h"

class FusionDHT11 : public FusionModule
{
    public:
        FusionDHT11(unsigned int ni, unsigned int sensorPin);

        DHT* dht;

        void update();
};
#endif

