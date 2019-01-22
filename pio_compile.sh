# PARAMS
WIFI_SSID="FUSION"
WIFI_PASSWORD='fusionjazz'
MQTT_SERVER='192.168.4.1'
MQTT_PORT=1883
#MQTT_USER="FUSION"
#MQTT_PASSWORD="fusionjazz"

NODE_NAME=$2
NODE_ID=$3
PIN=$4


mkdir nodes/pio/src
mkdir nodes/pio/lib
cp nodes/$1/* nodes/pio/src/
cp nodes/libraries/FUSION/* nodes/pio/lib
#mkdir nodes/$1/src/src
#mkdir nodes/$1/src/src/FUSION
#cp -r nodes/libraries/FUSION/* nodes/$1/src/src/FUSION
cd nodes/pio
export PLATFORMIO_BUILD_FLAGS="-DNODE_NAME=\"$NODE_NAME\" -DNODE_ID=$NODE_ID -DPIN=$PIN -DWIFI_SSID=\"$WIFI_SSID\" -DWIFI_PASSWORD=\"$WIFI_PASSWORD\" -DMQTT_SERVER=\"$MQTT_SERVER\" -DMQTT_PORT=$MQTT_PORT"
#export PLATFORMIO_BUILD_FLAGS='-DNODE_NAME="mucki" -DNODE_ID=40 -DPIN=5 -DWIFI_SSID="FUSION" -DWIFI_PASSWORD="fusionjazz" -DMQTT_SERVER="192.168.4.1" -DMQTT_PORT=1883'

#export PLATFORMIO_BUILD_FLAGS="-DNODE_NAME=$2"
echo $PLATFORMIO_BUILD_FLAGS
platformio run --target upload
rm -r src/*
#rm -r lib/*
cd ../..

