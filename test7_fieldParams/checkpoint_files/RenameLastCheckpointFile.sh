#!/usr/bin/env bash

for colNames in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi WoodyShrubsRiparianLo SedgeLo DwarfShrubsHi DwarfShrubsLo
do
	runname=$colNames
	checkpointsuffix='_05Dec18'
	dot='.'
	checkpointdirname=$runname$checkpointsuffix
	if [ -d "$checkpointdirname" ]; then
		exit
	fi
	mkdir $checkpointdirname
	for NUM in $(seq 1 32)
	do		
		cd ../$checkpointdirname$dot$NUM
		lastCp=$(ls -t checkpoint* | head -1)
		cd ../checkpoint_files/$checkpointdirname
		echo $runname" Run "$NUM
		endstr='checkpoint_last.h5'
		fname="$checkpointdirname$dot$NUM$endstr"
		cp ../../$checkpointdirname$dot$NUM/$lastCp $fname
		cd ../
	done
done
