#include <ESP8266WiFi.h>

#define INDEX_FRAME_BEGIN 0
#define INDEX_FRAME_ID 1
#define INDEX_MSG_ID 2
#define INDEX_NI 3
#define INDEX_NMB_DATA 4

#define FRAME_HEAD_LENGTH 4
#define FRAME_CHECKSUM_LENGTH 2
#define FRAME_BEGIN 0xAA
#define NODE_ID 36

const char* ssid = "FUSION";
const char* pw = "fusionjazz";
const unsigned int port = 5006;
const char* ip = "192.168.4.1";

WiFiClient tcpClient;

uint8_t pin_LED = D0;

void setup()
{
  pinMode(pin_LED, OUTPUT);

  Serial.begin(9600);
  Serial.println("beginning...");
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pw);
  
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println(".");
  }
  
  Serial.println("connected!");
}

void loop()
{
  checkConnection();
  digitalWrite(pin_LED, getLedStatus());



  /*byte result[2];
  byte buffer = tcpClient.read()
  while(buffer )
  if(result > -1) Serial.println(result, HEX);*/

  //Serial.println("done");
  
  delay(50);
}

void checkConnection()
{
  //Serial.println("checking connection...");
  if(!tcpClient.connected())
  {
    //Serial.println("reconnecting...");
    tcpClient.stop();
    if(!tcpClient.connect(ip, port))
    {
      //Serial.println("reconnect failed...");
      delay(500);
      return;
    }
  }
}

bool getLedStatus()
{
  int data_length = 1;
  int packet_length = data_length + 7;
  int index_checksum = 1 + FRAME_HEAD_LENGTH + data_length;
  char* packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);

  tcpClient.readBytes(packet, packet_length);

  bool result = (bool) packet[FRAME_HEAD_LENGTH + 1];
  return result;
}
/*
void sendButtonEvent(bool entered)
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

  
  
  tcpClient.write(packet, packet_length);
}
*/
