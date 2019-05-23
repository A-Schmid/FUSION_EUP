#!/bin/bash

# install required packages
sudo apt add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt update
sudo apt -y install libatlas-base-dev git python3-venv dnsmasq hostapd mosquitto mosquitto-clients

# install recommended packages
sudo apt -y install tmux nmap vim-gtk 

# set up python environment
python3 -m venv fusion-env
source fusion-env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# install python packages
pip install --upgrade pip
pip install jupyter
pip install numpy
pip install bokeh
pip install paho-mqtt
#pip install platformio
# install platformio dev version as the normal version does not support python3 yet
pip install -U https://github.com/platformio/platformio-core/archive/develop.zip

# configure platformio

echo "export PATH=$PATH:~/.platformio/penv/bin" >> ~/.bash_profile

# install platformio libraries
# maybe use -g for gloabl install?
cd nodes/pio
pio lib install 31 # Adafruit Unified Sensor
pio lib install 19 # DHT sensor library
pio lib install 89 # MQTT PubSubClient library
cd ../..

# add PIO udev rules
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/scripts/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo service udev restart

# configure jupyter
echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.ip = '*'" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py

# set up WiFi
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
sudo cp additional_files/install/dhcpcd.conf /etc/
sudo service dhcpcd restart

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo cp additional_files/install/dnsmasq.conf /etc/

sudo cp additional_files/install/hostapd.conf /etc/hostapd/hostapd.conf
sudo echo "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" >> /etc/default/hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

sudo cp additional_files/install/sysctl.conf /etc/

sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
sudo sed '19iiptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local

# access point

# existing


