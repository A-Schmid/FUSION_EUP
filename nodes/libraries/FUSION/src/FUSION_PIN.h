#ifndef FUSION_PIN_H
#define FUSION_PIN_H

#include "FUSION_MODULE.h"

class FusionPin : public FusionModule
{
    public:
        FusionPin(unsigned int pin_id);

        void initialize();
        void initialize(bool dir);

        unsigned int pin;

        void dWrite(bool value);
        bool dRead();

        void aWrite(uint16_t value);
        uint16_t aRead();
        
        void setDirection(bool dir);
        void setInterrupt(unsigned int edge);

        void onChange();
        void onRise();
        void onFall();

    private:
        const char* topic_pin;
        bool directionSet;
        bool direction;
        uint16_t lastValue;

        void mqttCallback(byte* payload, int length);
        
        //void registerCallbacks();
};

#endif
