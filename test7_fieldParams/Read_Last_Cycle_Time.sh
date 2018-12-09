#!/usr/bin/env bash

NUMBERS=$(seq 1 32)
runName='.'
echo $1$runName
for NUM in $NUMBERS
do
	cd $1$runName$NUM
	#cd run.$NUM
	echo 'Run #'$NUM
	tail -n 10000 stdout.out | grep Cycle | tail -1
	cd ../
done
