#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_DHT11.h"

FusionDHT11::FusionDHT11(unsigned int ni, unsigned int sensorPin) : FusionModule(ni)
{
    dht = new DHT(sensorPin, 11, 6);
    dht->begin();
}

void FusionDHT11::update()
{
    FusionModule::update();
    char* data = (char*)malloc(2); 
    data[0] = (char) dht->readHumidity();
    data[1] = (char) dht->readTemperature();
    sendData(data, 2);
    free(data);
}

