#!/usr/bin/env bash

NUMBERS=$(seq 1 18)
echo $NUMBERS
for NUM in $NUMBERS
do
	cd run.$NUM
	lastCp=$(ls -t checkpoint* | head -1)
	cp $lastCp checkpoint_last.h5
	cd ../
done
