#!/usr/bin/env bash

NUMBERS=$(seq 1 18)
echo $NUMBERS
for NUM in $NUMBERS
do
	m
	cd ../test7_matk/run.$NUM
	lastCp=$(ls -t checkpoint* | head -1)
	cp ../test7_matk/run.$NUM/
