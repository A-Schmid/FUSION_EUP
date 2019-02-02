#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "FUSION_GPIO.h"

FusionGPIO::FusionGPIO() : FusionModule()
{
    
}

void FusionGPIO::update()
{
    FusionModule::update();

    char* data = (char*)malloc(3); 

    int data_length = readPacket(data);

    if(data_length == 0)
    {
        return;
    }

    parseMessage(data);
}

int FusionGPIO::parseMessage(char* message)
{
    unsigned int pin = message[1];
    char* data;
    int result;

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
            aWrite(pin, ((message[2] << 8) | message[3]));
            break;
        case 3:
            result = dRead(pin);
            data = (char*) malloc(2);
            data[0] = (char) pin;
            data[1] = (char) result;
            sendData(data, 2);
            free(data);
            break;
        case 4:
            result = aRead(pin);
            data = (char*) malloc(3);
            data[0] = (char) pin;
            data[1] = (char) (result >> 8);
            data[2] = (char) (result);
            sendData(data, 3);
            //free(data);
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
    digitalRead(pin);
}

unsigned int FusionGPIO::aRead(unsigned int pin)
{
    return analogRead(pin);
}
