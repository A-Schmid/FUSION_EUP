#ifndef FUSION_WIFI_H
#define FUSION_WIFI_H

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define WIFI_MODE_UDP 1
#define WIFI_MODE_TCP 2

bool initWifi();
bool sendPacket(char* data, unsigned int length);
bool sendPacket(char* data, unsigned int length, unsigned int mode);

#endif // FUSION_WIFI_H
