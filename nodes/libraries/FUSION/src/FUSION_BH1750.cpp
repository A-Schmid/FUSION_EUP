#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_BH1750.h"
#include "Wire.h"

FusionBH1750::FusionBH1750() : FusionModule()
{
    length = 2;
    address = I2C_ADDR;

    //init();
    // TODO
}

void FusionBH1750::initialize()
{
    FusionModule::initialize();

    Wire.begin();

    delay(200); // TODO magic number

    Wire.beginTransmission(address);
    Wire.write(0x10);
    Wire.endTransmission();
}

int FusionBH1750::read(char* buffer, int len)
{
    int i = 0;
    
    Wire.beginTransmission(address);
    
    Wire.requestFrom(address, len);
    
    while(Wire.available() && i < len) 
    {
        buffer[i] = Wire.read();
        i++;
    }
    
    Wire.endTransmission();  

    return i;
}

void FusionBH1750::write()
{
    // TODO
}

uint16_t FusionBH1750::readLightIntensity()
{
    uint16_t value = 0;
    char* data = (char*) malloc(length); 

    if(read(data, length) == length)
    {
        value = ((data[0] << 8) | data[1]);
    }
    
    return value;
}

void FusionBH1750::update()
{
    // TODO
    FusionModule::update();

    int i;
    uint16_t value = 0;
    char* data = (char*) malloc(length); 

    // TODO restricted to length of 2 right now
    if(read(data, length) == length)
    {
        value = ((data[0] << 8) | data[1]); // TODO magic number
    }

    if(protocol == PROTOCOL_WIFI)
    {
        sendData(data, 2);
    }
    else if(protocol == PROTOCOL_MQTT)
    {
        sendData(value, "light_intensity");
    }
    free(data);
}

