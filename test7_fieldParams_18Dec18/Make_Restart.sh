#!/usr/bin/env bash

fname="AllColumns_$(date +"%Y_%m%d_%H%M").txt"
oldSuffix="_18Dec18_CrashedRuns"
checkpointSuffix=$oldSuffix
newSuffix="_18Dec18_CrashedRuns_2"
matkSuffix="_matk.py"
jssSuffix="_jss.sh"
touch $fname

echo "Filename: $fname"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	#sed -i "s/$runName$matkSuffix/$runName$oldSuffix$matkSuffix/g" $runName$oldSuffix$jssSuffix
	cp $runName$oldSuffix$matkSuffix $runName$newSuffix1$matkSuffix
	cp $runName$oldSuffix$jssSuffix $runName$newSuffix1$jssSuffix
	sed -i "/checkpointSuffix = /d" $runName$newSuffix1$matkSuffix
	sed -i "60i checkpointSuffix = '$checkpointSuffix'" $runName$newSuffix1$matkSuffix
	sed -i "s/'_template' + suffix + '$oldSuffix'/'_template' + '$newSuffix1'/g" $runName$newSuffix1$matkSuffix
	sed -i "s/$runName$oldSuffix$matkSuffix/$runName$newSuffix1$matkSuffix/g" $runName$newSuffix1$jssSuffix
	sed -i "s/workdir_base=runName + suffix + '$oldSuffix'/workdir_base=runName + '$newSuffix1'/g" $runName$newSuffix1$matkSuffix
done
