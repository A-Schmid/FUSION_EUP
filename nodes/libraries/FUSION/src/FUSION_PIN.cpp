#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_PIN.h"

// this abomination is needed because of how C++ handles member functions
// in order to have callbacks on member functions for ISR interrupts,
// we have to save all instances with callbacks in static data structures
// and trigger them over a this pointer
std::list<FusionPin*> FusionPin::interruptPins_change;
std::list<FusionPin*> FusionPin::interruptPins_rise;
std::list<FusionPin*> FusionPin::interruptPins_fall;

FusionPin::FusionPin(unsigned int pin_id) : FusionModule()
{
    pin = pin_id;
    isAnalog = (pin == A0); // has to be changed to match different architectures
    directionSet = false;
}

void FusionPin::initialize()
{
    char topic_with_pin[TOPIC_MAXLENGTH];
    
    FusionModule::initialize();

/*
    // this should not be used as it overwrites the mqtt object's topic
    // making it impossible to use multiple instances
    sprintf(topic_pin, "%d", pin);

    strcpy(topic_with_pin, STR(NODE_NAME)); 
    strcat(topic_with_pin, "/");
    strcat(topic_with_pin, topic_pin);

    strcpy(mqtt->topic_name, topic_with_pin);
*/
    registerCallbacks();
}

void FusionPin::initialize(bool dir)
{
    setDirection(dir);
    initialize();
}

// has to be called each loop cycle
void FusionPin::update()
{
    FusionModule::update();
    if(streamOn) streamData();
}

// register callbacks on supported MQTT topics
void FusionPin::registerCallbacks()
{
    char* callbackCommands[] = {
        "digitalRead",
        "digitalWrite",
        "analogRead",
        "analogWrite",
        "setDirection",
        "setInterrupt",
        "removeInterrupt",
        "streamData"
    };

    for(char* command : callbackCommands)
    {
        // I am sorry.
        // here I append the current pin and a slash to the beginning of the command
        // to fake a fifth entry in the mqtt topic
        // the callback now listens for pin/command
        char command_with_pin[TOPIC_MAXLENGTH];
        
        sprintf(command_with_pin, "%d", pin);
        strcat(command_with_pin, "/");
        strcat(command_with_pin, command);

        mqtt->registerCallback(std::bind(&FusionPin::mqttCallback, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3), command_with_pin);
    }
}

// handles MQTT messages
void FusionPin::mqttCallback(char* topic, byte* payload, int length)
{
    // extract payload from message
    uint16_t data;

    if(length == 1) data = payload[0] - '0';
    else if(length == 2) data = ((payload[1] - '0') << 8) | (payload[0] - '0');

    // check for command and call the corresponding function
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

// wrapper for Arduino digitalWrite()
void FusionPin::dWrite(bool value)
{
    digitalWrite(pin, value);
}

// wrapper for Arduino digitalRead()
bool FusionPin::dRead()
{
    bool data = digitalRead(pin);
    sendData(data, "digitalData");
    return data;
}

// wrapper for Arduino analogWrite()
void FusionPin::aWrite(uint16_t value)
{
    analogWrite(pin, value);
}

// wrapper for Arduino analogRead()
uint16_t FusionPin::aRead()
{
    uint16_t data = analogRead(pin);
    sendData(data, "analogData");
    return data;
}

// TODO test this
void FusionPin::streamData()
{
    long time = millis();
    if(time - streamTimer >= streamDelay)
    {
        streamTimer = time;
        isAnalog ? aRead() : dRead();
    }
}

// wrapper for Arduino pinMode()
void FusionPin::setDirection(bool dir)
{
    pinMode(pin, dir);

    direction = dir;
    directionSet = true;
}

// detaches all interrupts from this pin
void FusionPin::removeInterrupt()
{
    detachInterrupt(digitalPinToInterrupt(pin));

    // these flags are used to throw pins without interrupts out of the callback thingy
    interruptSet_change = false;
    interruptSet_rise = false;
    interruptSet_fall = false;
}

// attaches a new interrupt to this pin and registers it to the complicated callback workarond thing
void FusionPin::setInterrupt(unsigned int edge)
{
    pinMode(pin, INPUT_PULLUP);

    switch(edge)
    {
        case CHANGE:
            if(interruptSet_change) return; // it's already set, do nothing
            attachInterrupt(digitalPinToInterrupt(pin), interruptHandler_change, edge);
            interruptPins_change.push_back(this); // tell the callback thingy that this pin has an interrupt attached
            interruptSet_change = true; // make sure we don't attach multiple interrupts
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

// interrupt callback on rise or fall
void FusionPin::onChange()
{
    sendData(topic_pin, 2, "change");
}

// interrupt callback on rise
void FusionPin::onRise()
{
    sendData(topic_pin, 2, "rise");
}

// interrupt callback on fall
void FusionPin::onFall()
{
    sendData(topic_pin, 2, "fall");
}

// this is a unnecessary complicated workaround to get interrupts to work
// we can not register a member function as a callback for interrupts,
// so we have to use a static function.
// all members with interrupts attached are saved in a data structure
// and their callbacks are called here.
void FusionPin::interruptHandler_change()
{
    // loop over all pins with change interrupts attached
    for(auto it = interruptPins_change.begin(); it != interruptPins_change.end();) 
    {
        FusionPin *p = *it;

        // remove pin from the list, if the interrupt has been detached
        if(!p->interruptSet_change) 
        {
            it = interruptPins_change.erase(it);
            continue;
        }

        // otherwise, trigger the callback
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
