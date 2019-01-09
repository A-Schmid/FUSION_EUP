#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_BH1750.h"

FusionBH1750::FusionBH1750(unsigned int ni, int addr) : FusionModule(ni)
{
    length = 2;
    address = addr;

    init();
    // TODO
}

void FusionBH1750::init()
{
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

void FusionBH1750::update()
{
    // TODO
    FusionModule::update();

    int i;
    uint16_t value = 0;
    char* data = (char*) malloc(length); 

    //BH1750_Init(BH1750address);
    //delay(200);

    // TODO restricted to length of 2 right now
    if(read(data, length) == length)
    {
        value = ((data[0] << 8) | data[1]) / 1.2; // TODO magic number
        //Serial.print(val,DEC);     
        //Serial.println("[lx]"); 
    }

    sendData(data, 2);
    free(data);

    delay(150); // TODO maybe shorter is ok?
}

