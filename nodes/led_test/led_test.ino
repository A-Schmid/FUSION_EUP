#include <ESP8266WiFi.h>

#define INDEX_FRAME_BEGIN 0
#define INDEX_FRAME_ID 1
#define INDEX_MSG_ID 2
#define INDEX_NI 3
#define INDEX_NMB_DATA 4

#define FRAME_HEAD_LENGTH 4
#define FRAME_CHECKSUM_LENGTH 2
#define FRAME_BEGIN 0xAA
#define NODE_ID 42

const char* ssid = "FUSION";
const char* pw = "fusionjazz";
const unsigned int port = 5008;
const char* ip = "192.168.4.1";

WiFiClient tcpClient;

uint8_t pin_LED = D0;
bool accepted = false;

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
  while(!accepted)
  {
    Serial.println("waiting for acceptance...");
    checkConnection();
    sendHandshakePacket();
    accepted = true;
  }

  checkConnection();
  digitalWrite(pin_LED, getLedStatus());

  Serial.println("done");
  
  delay(50);
}

void checkConnection()
{
  Serial.println("checking connection...");
  if(!tcpClient.connected())
  {
    Serial.println("reconnecting...");
    tcpClient.stop();
    int connection = tcpClient.connect(ip, port);
    if(connection != 1)
    {
      Serial.println("reconnect failed...");
      delay(500);
      return;
    }
  }
}

void sendHandshakePacket()
{
  char packet[1];
  packet[0] = (char) NODE_ID;
  while(1)
  {
    Serial.print("sending handshake..."); Serial.println(packet[0], HEX);
    tcpClient.write(packet, 1);
    Serial.println("waiting for ack");
    delay(100); //necessary?
    char ack = tcpClient.read();
    Serial.println(ack, HEX);
    if(ack == 1)
    {
      Serial.println("ack: success!");
      break;
    }
    delay(500);
  }
}

bool getLedStatus()
{
  int data_length = -1;
  while(data_length == -1)
  {
    data_length = (int) tcpClient.read();
  }
  Serial.print("datalength: "); Serial.println(data_length);
  tcpClient.write(0x01);

  int packet_length = data_length + 7;
  int index_checksum = 1 + FRAME_HEAD_LENGTH + data_length;
  char* packet = (char*) malloc(2 + FRAME_HEAD_LENGTH + data_length + FRAME_CHECKSUM_LENGTH);

  tcpClient.readBytes(packet, packet_length);
  for(int i = 0; i < packet_length; i++)
  {
    Serial.print(packet[i], HEX); Serial.print(" ");
  }
  Serial.println("");
  Serial.print("led status: "); Serial.println(packet[FRAME_HEAD_LENGTH+1], HEX);
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
