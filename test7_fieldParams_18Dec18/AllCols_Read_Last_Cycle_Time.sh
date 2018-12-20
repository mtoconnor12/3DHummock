#!/usr/bin/env bash

fname="LastTimestep_$(date +"%Y_%m%d_%H%M").txt"
touch $fname
suffix="_18Dec18"
echo "Filename: $fname"

for colNames in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
        runName=$colNames
	NUMBERS=$(seq 1 32)
	dot='.'
	extension='.txt'
	echo $runName
	echo $runName >> $fname
	for NUM in $NUMBERS
	do
		cd $runName$suffix$dot$NUM
		echo 'Run #'$NUM >> ../$fname
		tail -n 15000 stdout.out | grep Cycle | tail -1  >> ../$fname
		cd ../
	done
done
