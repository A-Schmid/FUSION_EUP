#ifndef FUSION_WIFI_H
#define FUSION_WIFI_H

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define INDEX_FRAME_BEGIN 0
#define INDEX_MSG_TYPE 1
#define INDEX_MSG_ID 2
#define INDEX_NI 3
#define INDEX_NMB_DATA 4
#define INDEX_DATA 5

#define FRAME_HEAD_LENGTH 4
#define FRAME_CHECKSUM_LENGTH 2
#define FRAME_BEGIN 0xAA

#define MSG_TYPE_HANDSHAKE 0
#define MSG_TYPE_LENGTH 1
#define MSG_TYPE_PACKET 2

#define WIFI_MODE_UDP 1
#define WIFI_MODE_TCP 2

#define ssid "FUSION"
#define pw "fusionjazz"
#define ip "192.168.4.1"
#define udp_port 5005
#define tcp_port 5006

bool initWifi();
bool sendPacket(char* data, unsigned int length);
bool sendPacket(char* data, unsigned int length, unsigned int mode);
void sendHandshake(int node_id);
bool checkConnection();
int readPacket(char* data);
int readLengthPacket();

#endif // FUSION_WIFI_H
