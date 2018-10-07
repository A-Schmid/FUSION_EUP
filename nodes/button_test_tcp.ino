#define DEBUG 1
#include "libraries/FUSION/FUSION_Button.h"

bool wasDown = false;

uint8_t buttonPin = D3;

FusionButton button(buttonPin, 43);

void setup()
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  button.initialize();
}

void loop()
{
  button.checkButtonState();

  delay(50);
}
