#include "FUSION_UTILS.h"

// make sure all parameters are set
#ifndef DELAY
    #define DELAY 1000
#endif

int update_time = DELAY;

char* wifi_ssid = STR(WIFI_SSID);
char* wifi_password = STR(WIFI_PASSWORD);
char* mqtt_server = STR(MQTT_SERVER);
int mqtt_port = MQTT_PORT;

char* protocol = STR(PROTOCOL);

int node_id = NODE_ID;
