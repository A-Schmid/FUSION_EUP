#echo "xbee add sh start" >>/tmp/logfile.txt
path=$(env | grep "DEVNAME" | grep -o -P "(?<=DEVNAME=).*")
name=$(env | grep "ID_MODEL_FROM_DATABASE" | grep -o -P "(?<=ID_MODEL_FROM_DATABASE=).*" | tr -d '(' | tr -d ')' | tr -d '"' | tr ' ' '_')
#name=$(env | grep "ID_MODEL_FROM_DATABASE" | grep -o -P "(?<=ID_MODEL_FROM_DATABASE=).*")
#echo "blub" >>/tmp/test.log
#name="FT232_Serial_UART_IC"
#echo "$path" >>/tmp/logfile.txt
#echo "$name" >>/tmp/logfile.txt
#result=$(env | grep "DEVNAME" | grep -o -E "[0-9]+")
#echo "$result" >>/tmp/test.log
#echo $(env) >>/tmp/test.log
#optargs="$path:$name"
#echo "test">>"/tmp/$name.txt"
#mkdir "/tmp/fusisusi/$name"
mkdir "/dev/FUSION/$name"
python3 /usr/local/bin/FUSION/xbee_add.py $path "\"$name\"" &
#echo "py script started from sh" >> /tmp/logfile.txt
#echo "it worked" >>/tmp/test.log
