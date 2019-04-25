#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_LED.h"

FusionLed::FusionLed(unsigned int pin_id) : FusionModule()
{
    pin = pin_id;
    pinMode(pin, OUTPUT);
}

void FusionLed::initialize()
{
    FusionModule::initialize();

    mqtt->registerCallback(std::bind(&FusionLed::mqttCallback, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3), "led_state");
}

// has to be called each loop cycle
void FusionLed::update()
{
    FusionModule::update();
}

// handles MQTT messages
void FusionLed::mqttCallback(char* topic, byte* payload, int length)
{
    Serial.println(topic);

    // extract payload from message
    uint16_t data;

    if(length == 1) data = payload[0] - '0';
    else if(length == 2) data = ((payload[1] - '0') << 8) | (payload[0] - '0');

    digitalWrite(pin, data);
}
