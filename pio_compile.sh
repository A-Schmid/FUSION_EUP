. ./fusion.conf

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   

    case "$KEY" in
            NODE_NAME) NODE_NAME=${VALUE} ;;
            NODE_ID)   NODE_ID=${VALUE} ;;     
            PIN)       PIN=${VALUE} ;;     
            DELAY)     DELAY=${VALUE} ;;
            PROTOCOL)  PROTOCOL=${VALUE} ;;
            ACTION)    ACTION=${VALUE} ;;
            *)   
    esac    
done

mkdir nodes/pio/src
mkdir nodes/pio/lib
cp nodes/$1/* nodes/pio/src/
cp nodes/libraries/FUSION/* nodes/pio/lib
cd nodes/pio

export PLATFORMIO_BUILD_FLAGS="-DNODE_NAME=\"$NODE_NAME\" -DNODE_ID=$NODE_ID -DPIN=$PIN -DWIFI_SSID=\"$WIFI_SSID\" -DWIFI_PASSWORD=\"$WIFI_PASSWORD\" -DMQTT_SERVER=\"$MQTT_SERVER\" -DMQTT_PORT=$MQTT_PORT -DMQTT_TOPIC_NETWORK=\"$MQTT_TOPIC_NETWORK\" -DMQTT_TOPIC_LOCATION=\"$MQTT_TOPIC_LOCATION\" -DDELAY=$DELAY -DPROTOCOL=\"$PROTOCOL\""

echo $PLATFORMIO_BUILD_FLAGS
if [ $ACTION = "debug" ]; then
    echo "debug..."
    platformio run --target debug
else
    platformio run --target upload
fi

rm -r src/*
cd ../..

