#!/usr/bin/env bash

fname="AllColumns_$(date +"%Y_%m%d_%H%M").txt"
suffix="_18Dec18"
touch $fname

echo "Filename: $fname"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	NUMBERS=$(seq 1 32)
	dot='.'
	echo $runName
	# echo $runName >> $fname
	for NUM in $NUMBERS
	do
		if [ -d "$runName$suffix$dot$NUM" ];
		then
			cd $runName$suffix$dot$NUM
			#echo 'Run #'$NUM >> ../$fname
			stuff=$(tail -n 100 stdout.out | grep Cycle | tail -1)
			echo -e "$runName\t$NUM\t$stuff" >> ../$fname
			#sed -e "$NUM s/^/"$runName$underscore$NUM"/" -i ../$fnam
			cd ../
		else
			stuff="NO DATA HERE"
			echo -e "$runName\t$NUM\t$stuff" >> ../$fname
		fi
	done
done
