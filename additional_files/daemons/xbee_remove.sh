#echo "workserino">>/tmp/test.log
#echo "xbee remove sh" >> /tmp/logfile.txt
name=$(env | grep "ID_MODEL_FROM_DATABASE" | grep -o -P "(?<=ID_MODEL_FROM_DATABASE=).*" | tr -d '(' | tr -d ')' | tr -d '"' | tr ' ' '_')
#echo "/dev/FUSION/$name" >>/tmp/test.log
rm -r "/dev/FUSION/$name"

