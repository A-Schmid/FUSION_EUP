mkdir nodes/$1/src
mkdir nodes/$1/src/FUSION
cp -r nodes/libraries/FUSION/* nodes/$1/src/FUSION
sudo /home/schmid/Downloads/arduino-1.8.5/arduino --board esp8266:2.4.1:d1_mini:CpuFrequency=80,FlashSize=4M1M,UploadSpeed=921600 --port /dev/ttyUSB0 --upload nodes/$1/$1.ino
rm -r nodes/$1/src

