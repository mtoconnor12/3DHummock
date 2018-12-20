#!/usr/bin/env bash

NUMBERS=$(seq 1 32)
runName='.'
extension='.txt'
echo $1
touch $1$extension
for NUM in $NUMBERS
do
	cd $1$runName$NUM
	echo 'Run #'$NUM >> ../$1$extension
	tail -n 15000 stdout.out | grep Cycle | tail -1  >> ../$1$extension
	cd ../
done
