#!/bin/bash


## TODO
## initialize config files
#
## $MODE: create access point or use existing WiFi network
##   1) access point
##   2) use existing network
#
#echo "Do you want FUSION to create an access point or use an existing network?"
#echo "1) Access Point"
#echo "2) Existing"
#read MODE
#
#case "$MODE" in
#    1)
#        echo "AP"
#        break;;
#    2)
#        echo "WIFI"
#        break;;
#    *)
#        echo "$mode is not a valid choice"
#        break;;
#esac
#
#echo "enter the SSID of the WiFi network you want to use:"
#read SSID
#
#echo "enter the password of the WiFi network you want to use:"
#read -s PW
#
#exit
    


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


