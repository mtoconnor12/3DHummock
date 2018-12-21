#!/usr/bin/env bash

for colNames in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	runname=$colNames
	checkpointsuffix='_18Dec18_UncrashedRuns'
	dot='.'
	dotTwo='.0'
	checkpointdirname=$runname$checkpointsuffix
	if [ -d "$checkpointdirname" ]; then
		exit
	fi
	mkdir $checkpointdirname
	for NUM in $(seq 1 32)
	do		
		if [ -d "../$checkpointdirname$dot$NUM" ]
                then
			cd ../$checkpointdirname$dot$NUM
			lastCp=$(ls -t checkpoint* | head -1)
			cd ../checkpoint_files/$checkpointdirname
			echo $runname" Run "$NUM
			endstr='checkpoint_last.h5'
			fname="$checkpointdirname$dot$NUM$dotTwo$endstr"
			cp ../../$checkpointdirname$dot$NUM/$lastCp $fname
			cd ../
		else
			continue
		fi
	done
done
