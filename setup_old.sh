echo "Welcome to the FUSION setup script!"
echo "installing a lot of useful software..."
sudo apt update
sudo apt -y install fish
sudo apt -y install tmux
sudo apt -y install git
sudo apt -y install nmap
sudo apt -y install vim
sudo apt -y install libatlas-base-dev
sudo apt -y install python3-venv
echo "installing python related stuff..."
python3 -m venv fusion-env
source fusion-env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
echo "install required packages"
pip install --upgrade pip
pip install jupyter
pip install numpy
pip install bokeh
pip install bringbuf
pip install pyserial
pip install paho-mqtt
echo "configuring jupyter..."
configure jupyter
jupyter notebook --generate-config
jupyter notebook password
echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.ip = '*'" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py
echo "setting up the access point..."
sudo apt install dnsmasq hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
sudo echo "interface wlan0" >> /etc/dhcpcd.conf
sudo echo "    static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf
sudo echo "    nohook wpa_supplicant" >> /etc/dhcpcd.conf
sudo service dhcpcd restart
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo echo "interface=wlan0" >> /etc/dnsmasq.conf
sudo echo "    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h" >> /etc/dnsmasq.conf
sudo echo "interface=wlan0" >> /etc/hostapd/hostapd.conf
sudo echo "driver=nl80211" >> /etc/hostapd/hostapd.conf
sudo echo "ssid=FUSION" >> /etc/hostapd/hostapd.conf
sudo echo "hw_mode=g" >> /etc/hostapd/hostapd.conf
sudo echo "channel=7" >> /etc/hostapd/hostapd.conf
sudo echo "wmm_enabled=0" >> /etc/hostapd/hostapd.conf
sudo echo "macaddr_acl=0" >> /etc/hostapd/hostapd.conf
sudo echo "auth_algs=1" >> /etc/hostapd/hostapd.conf
sudo echo "ignore_broadcast_ssid=0" >> /etc/hostapd/hostapd.conf
sudo echo "wpa=2" >> /etc/hostapd/hostapd.conf
sudo echo "wpa_passphrase=fusionjazz" >> /etc/hostapd/hostapd.conf
sudo echo "wpa_key_mgmt=WPA-PSK" >> /etc/hostapd/hostapd.conf
sudo echo "wpa_pairwise=TKIP" >> /etc/hostapd/hostapd.conf
sudo echo "rsn_pairwise=CCMP" >> /etc/hostapd/hostapd.conf
sudo echo "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" >> /etc/default/hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq
sudo echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
sudo sed '19iiptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local
sudo echo "system is going to reboot NOW"
#sudo reboot
