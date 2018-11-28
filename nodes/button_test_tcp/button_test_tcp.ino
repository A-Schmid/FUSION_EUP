#define DEBUG 1
#include "FUSION_Button.h"

// needed?
bool wasDown = false;

uint8_t buttonPin = D3;

FusionButton button(buttonPin, NODE_ID);

void setup()
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  button.initialize();
}

void loop()
{
  button.checkButtonState();

  delay(button.wait_time);
}
