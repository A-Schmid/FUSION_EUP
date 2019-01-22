#define DEBUG 1
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "FUSION";
const char* password = "fusionjazz";

const char* mqttServer = "192.168.4.1";
const int mqttPort = 1883;
const char* mqttUser = "FUSION";
const char* mqttPassword = "fusionjazz";

const char* topic_network = "FUSION";
const char* topic_location = "1104";
const char* topic_name = "testi";
const char* topic_type = "testdata";

WiFiClient espClient;
PubSubClient client(espClient);

int data = 0;

void setup()
{
    Serial.begin(9600);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to the WiFi network");

    client.setServer(mqttServer, mqttPort);
    client.setCallback(callback);

    while (!client.connected()) {
        Serial.println("Connecting to MQTT...");

        if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {

            Serial.println("connected");  

        } else {

            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);

        }
    }

    client.subscribe("FUSION/test");
}

void loop()
{
    data += 1;
    client.publish("FUSION/test", "hello");
    client.loop();
    delay(5000);
}
 
void callback(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("-----------------------");
 
}
