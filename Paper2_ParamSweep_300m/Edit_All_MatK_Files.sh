#!/usr/bin/env bash


Suffix="_18Dec18"
matkSuffix="_matk.py"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	sed -i "29d" $runName$Suffix$matkSuffix
done
