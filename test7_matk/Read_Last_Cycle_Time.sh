#!/usr/bin/env bash

NUMBERS=$(seq 1 18)
for NUM in $NUMBERS
do
	cd CenturySim_20cmBC_Debug.$NUM
	#cd run.$NUM
	echo 'Run #'$NUM
	tail -n 5500 stdout.out | grep Cycle | tail -1
	cd ../
done
