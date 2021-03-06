#ifndef FUSION_UTILS_H
#define FUSION_UTILS_H

#define XSTR(x) #x
#define STR(x) XSTR(x)

#define PROTOCOL_WIFI "WIFI"
#define PROTOCOL_MQTT "MQTT"

#define TOPIC_UNDEFINED "undefined"
#define TOPIC_MAXLENGTH 128

extern int update_time;

extern char* wifi_ssid;
extern char* wifi_password;
extern char* mqtt_server;
extern int mqtt_port;

extern char* protocol;

extern int node_id;

#endif
