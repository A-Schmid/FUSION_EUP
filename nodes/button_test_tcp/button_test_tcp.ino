#define DEBUG 1
#include "FUSION_Button.h"

bool wasDown = false;

uint8_t buttonPin = D3;

FusionButton button(buttonPin, 43);

void setup()
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  button.initialize();
  sendHandshake(43);
}

void loop()
{
  button.checkButtonState();

  delay(50);
}
