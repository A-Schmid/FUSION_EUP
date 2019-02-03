#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_PIN.h"

FusionPin::FusionPin(unsigned int pin_id) : FusionModule()
{
    pin = pin_id;
    isAnalog = (pin == A0);
    directionSet = false;
}

void FusionPin::initialize()
{
    FusionModule::initialize();
    registerCallbacks();
}

void FusionPin::initialize(bool dir)
{
    setDirection(dir);
    initialize();
    
    snprintf(topic_pin, 2, "%d", pin);

    char topic[16];
    snprintf(topic, 16, "%d/#", pin);

    mqtt.registerCallback(&mqttCallback, topic);
}

void FusionPin::update()
{
    FusionModule::update();
    if(streamOn) streamData();
}

void FusionPin::mqttCallback(char* topic, byte* payload, int length)
{
    uint16_t data;

    if(length == 1) data = payload[0];
    else if(length == 2) data = (payload[1] << 8) | payload[0];

    if(topic.find("digitalRead" != -1) dRead();
    else if(topic.find("digitalWrite" != -1) dWrite((bool) data);
    else if(topic.find("analogRead" != -1) aRead();
    else if(topic.find("analogWrite" != -1) aRead(data);
    else if(topic.find("setDirection" != -1) setDirection((bool) data);
    else if(topic.find("streamData" != -1)
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
    sendData(topic_pin, data);
    return data;
}

void FusionPin::aWrite(uint16_t value)
{
    analogWrite(pin, value);
}

uint16_t FusionPin::aRead()
{
    uint16_t data = analogRead(pin);
    sendData(topic_pin, data);
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
    pinMode(pin, direction);

    direction = dir;
    directionSet = true;
}

void FusionPin::setInterrupt(unsigned int edge)
{
    void* callback;

    pinMode(pin, INPUT_PULLUP);

    switch(edge)
    {
        case CHANGE:
            callback = &onChange;
            break;
        case RISING:
            callback = &onRise;
            break;
        case FALLING;
            callback = &onFall;
            break;
    }

    attachInterrupt(digitalPinToInterrupt(pin), *callback, edge);
    directionSet = true;
    direction = INPUT;
}

void FusionPin::onChange()
{
    sendData(topic_pin, "change");
}

void FusionPin::onRise()
{
    sendData(topic_pin, "rise");
}

void FusionPin::onFall()
{
    sendData(topic_pin, "fall");
}
