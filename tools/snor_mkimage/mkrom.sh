#!/bin/bash

MAIN_PATH=../../..
BUILD_CR5_PATH=/cr5-bsp/sources/build/tcc805x/gcc/tcc805x-freertos-debug
TCC8050_CFG=tcc8050.cs.cfg

SNOR_MKIMAGE_PATH=`dirname "$0"`
pushd $SNOR_MKIMAGE_PATH

#Get r5_fw.rom
if [ -f "$MAIN_PATH$BUILD_CR5_PATH/r5_fw.rom" ]; then
	echo "Get r5_fw.rom"
	cp $MAIN_PATH$BUILD_CR5_PATH/r5_fw.rom .

	#Make snor image
	./tcc805x-snor-mkimage -i $TCC8050_CFG -o $MAIN_PATH$BUILD_CR5_PATH/cr5_snor.rom
	rm -rf r5_fw.rom
else
	echo "Please build cr5 first"
	popd
	exit
fi

popd