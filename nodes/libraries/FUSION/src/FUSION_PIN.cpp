#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_PIN.h"

std::list<FusionPin*> FusionPin::interruptPins_change;
std::list<FusionPin*> FusionPin::interruptPins_rise;
std::list<FusionPin*> FusionPin::interruptPins_fall;

FusionPin::FusionPin(unsigned int pin_id) : FusionModule()
{
    pin = pin_id;
    isAnalog = (pin == A0);
    directionSet = false;
}

void FusionPin::initialize()
{
    FusionModule::initialize();
    
    snprintf(topic_pin, 2, "%d", pin);

    registerCallbacks();
}

void FusionPin::initialize(bool dir)
{
    setDirection(dir);
    initialize();
}

void FusionPin::update()
{
    FusionModule::update();
    if(streamOn) streamData();
}

void FusionPin::registerCallbacks()
{
    char* commands[] = {"digitalRead", "digitalWrite", "analogRead", "analogWrite", "setDirection", "setInterrupt", "removeInterrupt", "streamData"};

    for(char* command : commands)
    {
        mqtt.registerCallback(std::bind(&FusionPin::mqttCallback, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3), command);
    }
}

void FusionPin::mqttCallback(char* topic, byte* payload, int length)
{
    uint16_t data;

    if(length == 1) data = payload[0] - '0';
    else if(length == 2) data = ((payload[1] - '0') << 8) | (payload[0] - '0');

    if(strstr(topic, "digitalRead")) dRead();
    else if(strstr(topic, "digitalWrite")) dWrite((bool) data);
    else if(strstr(topic, "analogRead")) aRead();
    else if(strstr(topic, "analogWrite")) aWrite(data);
    else if(strstr(topic, "setDirection")) setDirection((bool) data);
    else if(strstr(topic, "setInterrupt")) setInterrupt((unsigned int) data);
    else if(strstr(topic, "removeInterrupt")) removeInterrupt();
    else if(strstr(topic, "streamData"))
    {
        streamOn = true;
        streamDelay = data;
        streamTimer = millis();
    }
}

void FusionPin::dWrite(bool value)
{
    digitalWrite(pin, value);
}

bool FusionPin::dRead()
{
    bool data = digitalRead(pin);
    sendData(data, "digitalReadResult");
    return data;
}

void FusionPin::aWrite(uint16_t value)
{
    analogWrite(pin, value);
}

uint16_t FusionPin::aRead()
{
    uint16_t data = analogRead(pin);
    sendData(data, "analogReadResult");
    return data;
}

void FusionPin::streamData()
{
    long time = millis();
    if(time - streamTimer >= streamDelay)
    {
        streamTimer = time;
        isAnalog ? aRead() : dRead();
    }
}

void FusionPin::setDirection(bool dir)
{
    pinMode(pin, dir);

    direction = dir;
    directionSet = true;
}

void FusionPin::removeInterrupt()
{
    detachInterrupt(digitalPinToInterrupt(pin));
    interruptSet_change = false;
    interruptSet_rise = false;
    interruptSet_fall = false;
}

void FusionPin::setInterrupt(unsigned int edge)
{
    pinMode(pin, INPUT_PULLUP);

    switch(edge)
    {
        case CHANGE:
            if(interruptSet_change) return;
            attachInterrupt(digitalPinToInterrupt(pin), interruptHandler_change, edge);
            interruptPins_change.push_back(this);
            interruptSet_change = true;
            break;
        case RISING:
            if(interruptSet_rise) return;
            attachInterrupt(digitalPinToInterrupt(pin), interruptHandler_rise, edge);
            interruptPins_rise.push_back(this);
            interruptSet_rise = true;
            break;
        case FALLING:
            if(interruptSet_fall) return;
            attachInterrupt(digitalPinToInterrupt(pin), interruptHandler_fall, edge);
            interruptPins_fall.push_back(this);
            interruptSet_fall = true;
            break;
    }

    directionSet = true;
    direction = INPUT;
}

void FusionPin::onChange()
{
    sendData(topic_pin, 2, "change");
}

void FusionPin::onRise()
{
    sendData(topic_pin, 2, "rise");
}

void FusionPin::onFall()
{
    sendData(topic_pin, 2, "fall");
}

void FusionPin::interruptHandler_change()
{
    for(auto it = interruptPins_change.begin(); it != interruptPins_change.end();) 
    {
        FusionPin *p = *it;

        if(!p->interruptSet_change) 
        {
            it = interruptPins_change.erase(it);
            continue;
        }

        p->onChange();
        ++it;
    }
}

void FusionPin::interruptHandler_rise()
{
    for(auto it = interruptPins_rise.begin(); it != interruptPins_rise.end();)
    {
        FusionPin *p = *it;

        if(!p->interruptSet_rise) 
        {
            it = interruptPins_rise.erase(it);
            continue;
        }

        p->onRise();
        ++it;
    }
}

void FusionPin::interruptHandler_fall()
{
    for(auto it = interruptPins_fall.begin(); it != interruptPins_fall.end();)
    {
        FusionPin *p = *it;

        if(!p->interruptSet_fall) 
        {
            it = interruptPins_fall.erase(it);
            continue;
        }

        p->onFall();
        ++it;
    }
}
