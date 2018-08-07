#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define INDEX_FRAME_BEGIN 0
#define INDEX_FRAME_ID 1
#define INDEX_MSG_ID 2
#define INDEX_NI 3
#define INDEX_NMB_DATA 4

#define FRAME_HEAD_LENGTH 4
#define FRAME_CHECKSUM_LENGTH 2
#define FRAME_BEGIN 0xAA
#define NODE_ID 33

const char* ssid = "FUSION";
const char* pw = "fusionjazz";
const unsigned int port = 5005;
const char* ip = "192.168.4.1";

WiFiUDP udp;

char heartbeat = 0;

bool isTracked = false;

uint8_t motionPin = D1;

void setup()
{
  pinMode(motionPin, INPUT);

  Serial.begin(9600);
  Serial.println("beginning...");
  
  WiFi.begin(ssid, pw);
  
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println(".");
  }
  
  Serial.println("connected!");

  udp.begin(port);
  
  Serial.println("udp connected!");
}

void loop()
{
  bool motion = digitalRead(motionPin);
  if(motion == HIGH)
  {
    if(isTracked == false)
    {
      isTracked = true;
      Serial.println("enter");
      sendTrackingEvent(true);
    }
  }
  else
  {
    if(isTracked == true)
    {
      isTracked = false;
      Serial.println("leave");
      sendTrackingEvent(false);
    }
  }

  heartbeat++;
  delay(1000);
}

void sendTrackingEvent(bool entered)
{
  int data_length = 1;
  int packet_length = data_length + 7;
  int index_checksum = 1 + FRAME_HEAD_LENGTH + data_length;
  char* packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);
  
  packet[INDEX_FRAME_BEGIN] = FRAME_BEGIN;
  packet[INDEX_FRAME_ID] = heartbeat;
  packet[INDEX_MSG_ID] = 0;
  packet[INDEX_NI] = NODE_ID;
  packet[INDEX_NMB_DATA] = data_length;
  packet[1 + FRAME_HEAD_LENGTH] = entered;
  packet[index_checksum] = 1;
  packet[index_checksum + 1] = 1;
  packet[index_checksum + 2] = 0; // why?

  for(int i = 0; i < packet_length; i++)
  {
    Serial.println(packet[i], HEX);
  }
  Serial.println("-----");

  udp.beginPacket(ip, port);
  udp.write(packet, packet_length);
  udp.endPacket();
}

