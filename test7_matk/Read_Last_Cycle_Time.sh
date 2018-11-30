#!/usr/bin/env bash

NUMBERS=$(seq 1 18)
for NUM in $NUMBERS
do
	cd CenturySim_29Nov18.$NUM
	#cd run.$NUM
	echo 'Run #'$NUM
	tail -n 10000 stdout.out | grep Cycle | tail -1
	cd ../
done
