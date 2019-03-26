import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("FUSION/#")

def on_message(client, userdata, msg):
    #print("---")
    #print(int.from_bytes(msg.payload, "big", signed=False))
    #print(msg)
    #print(msg.payload)
    #print(type(msg.payload))
    #print(len(msg.payload))
    #print(ord(msg.payload))
    #data = msg.payload.decode()
    #data = struct.unpack("<cc", msg.payload)
    #print(data)
    #print(msg.topic)
    print("{} {}".format(msg.topic, msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

