#ifndef FUSION_PIN_H
#define FUSION_PIN_H

#include "FUSION_MODULE.h"

class FusionPin : public FusionModule
{
    public:
        FusionPin(unsigned int pin_id);

        void initialize();
        void initialize(bool dir);

        void update();

        unsigned int pin;

        void dWrite(bool value);
        bool dRead();

        void aWrite(uint16_t value);
        uint16_t aRead();

        void streamData();
        
        void setDirection(bool dir);
        void setInterrupt(unsigned int edge);
        void removeInterrupt();

        void onChange();
        void onRise();
        void onFall();

    private:
        char topic_pin[2];
        bool isAnalog;
        bool directionSet;
        bool direction;
        //uint16_t lastValue;

        bool streamOn;
        int streamDelay;
        long streamTimer;

        void registerCallbacks();

        void mqttCallback(char* topic, byte* payload, int length);

        bool interruptSet_change;
        bool interruptSet_rise;
        bool interruptSet_fall;

        static void interruptHandler_change();
        static void interruptHandler_rise();
        static void interruptHandler_fall();

        static std::list<FusionPin*> interruptPins_change;
        static std::list<FusionPin*> interruptPins_rise;
        static std::list<FusionPin*> interruptPins_fall;
};

#endif
