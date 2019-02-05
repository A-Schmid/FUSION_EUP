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
    //registerCallbacks();
    
    snprintf(topic_pin, 2, "%d", pin);

    char topic[16];
    snprintf(topic, 16, "%d/#", pin);

    //mqtt.registerCallback(this->mqttCallback, topic);
    //
    //
    //#if defined(ESP8266) || defined(ESP32)
    //#include <functional>
    //#define MQTT_CALLBACK_SIGNATURE std::function<void(char*, uint8_t*, unsigned int)> callback
    //#else
    //#define MQTT_CALLBACK_SIGNATURE void (*callback)(char*, uint8_t*, unsigned int)
    //#endif

    // TODO test this!
    mqtt.registerCallback(std::bind(&FusionPin::mqttCallback, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3), topic);
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

void FusionPin::mqttCallback(char* topic, byte* payload, int length)
{
    uint16_t data;

    if(length == 1) data = payload[0];
    else if(length == 2) data = (payload[1] << 8) | payload[0];

    if(strstr(topic, "digitalRead")) dRead();
    else if(strstr(topic, "digitalWrite")) dWrite((bool) data);
    else if(strstr(topic, "analogRead")) aRead();
    else if(strstr(topic, "analogWrite")) aWrite(data);
    else if(strstr(topic, "setDirection")) setDirection((bool) data);
    else if(strstr(topic, "streamData"))
    {
        streamOn = true;
        streamDelay = data;
        streamTimer = millis();
    }
    /*
    if(topic.find("digitalRead") != -1) dRead();
    else if(topic.find("digitalWrite") != -1) dWrite((bool) data);
    else if(topic.find("analogRead") != -1) aRead();
    else if(topic.find("analogWrite") != -1) aRead(data);
    else if(topic.find("setDirection") != -1) setDirection((bool) data);
    else if(topic.find("streamData") != -1)
    {
        streamOn = true;
        streamDelay = data;
        streamTimer = millis();
    }*/
}

void FusionPin::dWrite(bool value)
{
    digitalWrite(pin, value);
}

bool FusionPin::dRead()
{
    bool data = digitalRead(pin);
    sendData(data, topic_pin);
    return data;
}

void FusionPin::aWrite(uint16_t value)
{
    analogWrite(pin, value);
}

uint16_t FusionPin::aRead()
{
    uint16_t data = analogRead(pin);
    sendData(data, topic_pin);
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
    pinMode(pin, INPUT_PULLUP);

    switch(edge)
    {
        case CHANGE:
            //attachInterrupt(digitalPinToInterrupt(pin), std::bind(&FusionPin::onChange, this));
            break;
        case RISING:
            //attachInterrupt(digitalPinToInterrupt(pin), onRise, edge);
            break;
        case FALLING:
            //attachInterrupt(digitalPinToInterrupt(pin), onFall, edge);
            break;
    }

    directionSet = true;
    direction = INPUT;
}

void FusionPin::onChange()
{
    sendData("change", topic_pin);
}

void FusionPin::onRise()
{
    sendData("rise", topic_pin);
}

void FusionPin::onFall()
{
    sendData("fall", topic_pin);
}
