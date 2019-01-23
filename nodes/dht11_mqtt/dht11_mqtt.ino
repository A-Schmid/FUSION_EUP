#define DEBUG 1
#include "FUSION_MODULE.h"
#include "FUSION_MQTT.h"

uint8_t sensorPin = D4;

DHT* sensor;
FusionMQTT mqtt;

void setup()
{
    Serial.begin(9600);
    sensor = new DHT(sensorPin, 11, 6);
    sensor->begin();
    mqtt = FusionMQTT();
    mqtt.init();
}

void loop()
{
    char humi = sensor->readHumidity();
    char temp = sensor->readTemperature();
    char* test = "a";
    char* test2 = (char*)malloc(1);
    test2[0] = 15;
    char* test3 = (char*)malloc(3);
    test3[0] = 0xAA;
    test3[1] = 0xBB;
    test3[2] = 0xCC;
    mqtt.send("temperature", &temp, 1);
    mqtt.send("humidity", &humi, 1);
    mqtt.send("test", test, 1);
    mqtt.send("test2", test2, 1);
    mqtt.send("test3", test3, 3);
    //Serial.print("humi "); Serial.println(humi, DEC);
    //Serial.print("temp "); Serial.println(temp, DEC);
    delay(5000);
}
