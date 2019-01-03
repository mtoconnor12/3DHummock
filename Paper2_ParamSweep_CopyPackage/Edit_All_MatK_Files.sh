#!/usr/bin/env bash


Suffix="_18Dec18"
matkSuffix="_matk.py"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	sed -i "s/'Paper2_template_AllDefault.xml'/'Paper2_NoCheckpoint_NoVerbosity_Default.xml/g" $runName$Suffix$matkSuffix
done
