echo "starting udp receiver daemon..."
sudo python3 /usr/local/bin/FUSION/udp_receiver.py &
#echo "starting tcp sender daemon..."
#nohup sudo python3 /usr/local/bin/FUSION/tcp_sender.py &
echo "starting tcp receiver daemon..."
nohup sudo python3 /usr/local/bin/FUSION/tcp_receiver.py &
echo "starting jupyter notebook..."
jupyter notebook 
echo "all services up and running!"
exit
