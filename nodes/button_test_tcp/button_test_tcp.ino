void setup()
{
pinMode(D4, OUTPUT);
digitalWrite(D4, HIGH);
}

void loop()
{
}

/*#include "FUSION_WIFI.h"
#include "FUSION_MODULE.h"

bool wasDown = false;

uint8_t buttonPin = D3;

void setup()
{
  NODE_ID = 43;
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  if(initWifi() == true) Serial.println("connected!");
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
  char* packet;
  char data[1] = {(char) entered};
  unsigned int packet_length = createPacket(data, 1, packet);
  sendPacket(packet, packet_length);
}
*/
