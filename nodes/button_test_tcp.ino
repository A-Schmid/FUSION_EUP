#define DEBUG 1
#include "./src/FUSION/FUSION_MODULE.h"

bool wasDown = false;

uint8_t buttonPin = D3;

FusionModule module(43);

void setup()
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  module.initialize();
}

void loop()
{
  bool buttonDown = digitalRead(buttonPin);
  if(buttonDown == LOW)
  {
    if(wasDown == false)
    {
      wasDown = true;
      Serial.println("pressed");
      sendButtonEvent(true);
    }
  }
  else
  {
    if(wasDown == true)
    {
      wasDown = false;
      Serial.println("released");
      sendButtonEvent(false);
    }
  }

  delay(50);
}

void sendButtonEvent(bool entered)
{
  module.sendData(entered);
}
