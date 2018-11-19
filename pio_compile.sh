mkdir nodes/pio/src
mkdir nodes/pio/lib
cp nodes/$1/* nodes/pio/src/
cp nodes/libraries/FUSION/* nodes/pio/lib
#mkdir nodes/$1/src/src
#mkdir nodes/$1/src/src/FUSION
#cp -r nodes/libraries/FUSION/* nodes/$1/src/src/FUSION
cd nodes/pio
export PLATFORMIO_BUILD_FLAGS="-DNODE_ID=$2"
platformio run --target upload
rm -r src/*
#rm -r lib/*
cd ../..
