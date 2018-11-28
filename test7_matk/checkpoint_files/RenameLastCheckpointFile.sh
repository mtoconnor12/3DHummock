#!/usr/bin/env bash

NUM=1
runname='CenturySim_20cmBC_Debug_27Nov18.'
checkpointdirname='CenturySim_20cmBC_Debug_27Nov18_checkpoint_files'
if [ -d "$checkpointdirname" ]; then
	exit
fi
mkdir $checkpointdirname
for VARA in 0.01 0.1
do
	for VARB in 0.01 0.1 0.22
	do
		for VARC in 0.02 0.14 0.4
		do	
			cd ../$runname$NUM
			lastCp=$(ls -t checkpoint* | head -1)
			cd ../checkpoint_files/$checkpointdirname
			echo "Start"
			echo $VARA
			echo $VARB				
			echo $VARC
			str1='checkpoint_hillslope-30mSuite-'
			str2='m_'
			str3='bac_'
			str4='bct.h5'
			fname="$str1$VARA$str2$VARB$str3$VARC$str4"
			cp ../../$runname$NUM/$lastCp $fname
			cd ../
			NUM=$((NUM + 1))
		done
	done
done
