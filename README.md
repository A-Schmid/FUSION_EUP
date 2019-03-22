# FUSION_EUP
WIP! End User Programming Interface for the Open Source Project FUSION (http://fusion-project.io/).

### Setup ###

The EUP interface for FUSION can be run on most Linux systems. It is recommended to use a SOC platform like the Raspberry Pi as a gateway. Communication between sensor nodes and gateway happens over TCP/IP using WiFi for most cases. In default configuration, the gateway will create an access point which nodes will connect to. The MQTT protocol is used to transmit data in a structured way.
Configuration parameters like WiFi credentials and MQTT parameters are defined in the "fusion.conf" config file. This file is read by the upload script for sensor nodes.
Content of "fusion.conf":
    * WIFI_SSID: SSID of the access point
    * WIFI_PASSWORD: password of the access point - has to be at least 8 characters
    * MQTT_SERVER: IP address of the gateway (default: '192.168.4.1')
    * MQTT_PORT: port to be used by MQTT (default: 1883)
    * MQTT_USER: TODO
    * MQTT_PASSWORD: TODO
    * MQTT_TOPIC_NETWORK: first entry of the MQTT topic - it is used to distinguish different enclosed networks
    * MQTT_TOPIC_LOCATION: second entry of the MQTT topic - it is used to specify a node's physical location

The automatic installation script "setup.sh" (not entirely tested yet!) can be used for a quick installation and setup of required an recommended components to run the sensor network. The setup process consists of following steps:
    * installation of required and recommended packages using apt
    * setting up the python environment and installation of python packages using pip
    * setting up the platformio command line interface which is used to flash sensor nodes
    * configuring jupyter notebooks
    * setting up dnsmasq and hostapd to create a WiFi access point

### programming sensor nodes ###

The "nodes" directory contains code for sensor nodes in the form of Arduino style C++ files.
The "libraries" subdirectory contains the library used for those nodes which takes care of communication and wraps several different types of sensors. This library can be used to easily program different sensor nodes without having to care about advanced technical aspects.
The "pio" subdirectory is used by the upload script described later, do not touch this one.
Each other subdirectory contains code for a specific type of sensor node. It has to contain a ".ino" file with the same filename as the directory.

The upload script "pio_compile.sh" is used to flash programs onto sensor nodes. By default, Wemos D1 mini are used as sensor nodes, but platformIO supports several different platforms (hence the name I guess).
The script reads command line parameters as well as the "fusion.conf", copies the selected sensor node into the "nodes/pio" directory, calls platformIO to compile and upload the program to the sensor node and cleans up afterwards.

Usage (in the FUSION_EUP root directory):

```
sh pio_compile.sh [node] [param1=value param2=value ...]
```

Parameters:
    * NODE_NAME: custom name of the node, used as third part of the MQTT topic. Select whatever you want.
    * NODE_ID: [deprecated?] numeric ID of a node, was used by the old communication protocol and is still used for UDP and XBEE communication. Might be automated in the future, feel free to leave this away if you plan to use TCP.
    * PIN: [TODO] pin number for GPIO nodes. Maybe this is not needed anymore.
    * DELAY: time in milliseconds to wait after each update of the sensor.
    * PROTOCOL: protocol to use. Options: MQTT, [TODO]
    * ACTION: action the upload script has to execute:
        * debug: compile the program without uploading it
        * upload: [default] compile and upload the program

All of those parameters except ACTION as well as the contents of "fusion.conf" are passed to the program as compile time parameters and can be called from within the program. Feel free to extend the upload script by adding custom parameters and passing them as "-DPARAM=\"whatever\"" in the PLATFORMIO_BUILD_FLAGS.

### Using the FUSION library ###

The "FUSION" subdectory contains the python package "FUSION" which can be used to communicate with the sensor nodes. The main components of the library are models of specific sensors and utility classes to process/visualize data and wrap useful functions like sending e-mail or logging data. The library can be used in any python application including jupyter notebooks - which is the recommended way of usage.

Usage:

    * run "jupyter notebook" in the FUSION_EUP root directory
    * open the notebook in a web browser
    * create a python3 notebook
    * import desired modules of the FUSION library (from FUSION import [module])
    * create a new instance of the imported class

Depending on the type of module, you can register callbacks for events of the sensor, poll sensor data in a loop or call functions of actors.
Communication and other technical aspects are all handled by the library. If you want to explore the internal workings of the library, take a look at "FUSION_MQTT.py". Several global constants and settings are defined in "config.py".
To write custom modules, it is recommended to extend the FUSION_MQTT class. For simple sensors, it might be sufficient to only add data entries for the sensor's supported data fields in the new module's constructor. Take a look at "BH1750_MQTT.py" for a very simple example.
The data entry is a basically a string to identify the type of data it represents. It forms the fourth part of the MQTT topic. The sensor node broadcasts data under this topic which is received by FUSION modules listening for this data entry.
Read the last received value for a data entry using "module_instance.get("entry")" or register callbacks for updates of data on this entry using "module_instance.OnUpdate(callback_function, "entry")". No parameters are passed to the callback, so you have to call get() in your callback.

