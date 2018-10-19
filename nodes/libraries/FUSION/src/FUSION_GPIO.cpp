#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_GPIO.h"

FusionGPIO::FusionGPIO(unsigned int ni) : FusionModule(ni)
{
    
}

void FusionGPIO::update()
{
    char* data = (char*)malloc(3); 
    int data_length = readPacket(data);
    parseMessage(data);
    free(data);
}

int FusionGPIO::parseMessage(char* message)
{
    unsigned int pin = message[1];
    int result = -1;
    switch(message[0])
    {
        case 0:
            if(message[2] == 0) setDirection(pin, INPUT);
            else setDirection(pin, OUTPUT);
            break;
        case 1:
            dWrite(pin, message[2]);
            break;
        case 2:
            aWrite(pin, message[2]);
            break;
        case 3:
            result = dRead(pin);
            sendData(result);
            break;
        case 4:
            result = aRead(pin);
            sendData(result);
            break;
    }
    return result;
}

void FusionGPIO::setDirection(unsigned int pin, unsigned int direction)
{
    pinMode(pin, direction);
}

void FusionGPIO::dWrite(unsigned int pin, unsigned int value)
{
    digitalWrite(pin, value);
}

void FusionGPIO::aWrite(unsigned int pin, unsigned int value)
{
    analogWrite(pin, value);
}

bool FusionGPIO::dRead(unsigned int pin)
{
    return digitalRead(pin);
}

unsigned int FusionGPIO::aRead(unsigned int pin)
{
    return analogRead(pin);
}
