#!/usr/bin/env bash

NUMBERS=$(seq 1 18)
for NUM in $NUMBERS
do
	#cd run_fromCheckpoint_1Nov18.$NUM
	cd run.$NUM
	echo 'Run #'$NUM
	tail -n 1400 stdout.out | grep Cycle | tail -1
	cd ../
done
