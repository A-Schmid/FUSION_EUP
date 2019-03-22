# FUSION_EUP
WIP! End User Programming Interface for the Open Source Project FUSION (http://fusion-project.io/).

### WIP! Setup ###

You might want to try the new install script (not tested yet!):
$ sudo sh install.sh
make sure to run it from the FUSION_EUP directory (check with pwd)

 * clone the repo to your gateway (might be any linux system, tested with a RPi 3)
 * for xbee support:
   * install bRingBuf, numpy and pyserial python packages
   * add a udev rule for the FTDI usb thing; this rule will start and end the xbee daemon ones it's plugged in or unplugged:
   * $ cp additional_files/udev/98-FUSION.rules /etc/udev/rules.d/
   * add a directory for the daemon scripts:
   * $ mkdir /usr/local/bin/FUSION
   * copy the daemon scrips to the folder where the udev rule is expecting them:
   * $ cp additional_files/daemons/* /usr/local/bin/FUSION/
   * plug in the FTDI usb thing and hopefully the daemon starts
 * for UDP support:
   * set up a wifi network on your gateway (i called mine fusion): https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md 
   * ssid and pw of your network have to be hardcoded into the sensor nodes at the moment
   * run the UDP daemon as root and you're good to go
   * $ sh additional_files/scripts/start_udp.sh

### actually doing stuff ###

 * run $ jupyter notebook in the FUSION_EUP folder
 * create a new notebook
 * add the line
    from FUSION import *
   to your notebook
 * you can use all classes and functions of the API now

### setting up UDP nodes ###

 * see an example file (pir sensor with a ESP8266 via UDP) in the nodes directory
 TODO: actual documentation

