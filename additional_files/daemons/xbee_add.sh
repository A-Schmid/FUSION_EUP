path=$(env | grep "DEVNAME" | grep -o -P "(?<=DEVNAME=).*")
name=$(env | grep "ID_MODEL_FROM_DATABASE" | grep -o -P "(?<=ID_MODEL_FROM_DATABASE=).*" | tr -d '(' | tr -d ')' | tr -d '"' | tr ' ' '_')
#name=$(env | grep "ID_MODEL_FROM_DATABASE" | grep -o -P "(?<=ID_MODEL_FROM_DATABASE=).*")
#echo "blub" >>/tmp/test.log
#echo "$path" >>/tmp/test.log
#echo "$name" >>/tmp/test.log
#result=$(env | grep "DEVNAME" | grep -o -E "[0-9]+")
#echo "$result" >>/tmp/test.log
#echo $(env) >>/tmp/test.log
#optargs="$path:$name"
mkdir "/dev/FUSION/$name"
python3 /usr/local/bin/FUSION/xbee_add.py $path "\"$name\"" &
#echo "it worked" >>/tmp/test.log
