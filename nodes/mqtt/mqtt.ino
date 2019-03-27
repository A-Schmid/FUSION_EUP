//#include "FUSION_MODULE.h"
#include "FUSION_MQTT.h"

/*
 * this is an example of how the barebone MQTT module can be used to send data
 */

FusionMQTT mqtt;

char data = 0;

void setup()
{
    mqtt = FusionMQTT();
    mqtt.init();
}

void loop()
{
    data += 1;
    mqtt.send(&data, 1, "data");
    delay(update_time);
}
