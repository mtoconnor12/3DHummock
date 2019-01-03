#!/usr/bin/env bash


Suffix="_18Dec18"
matkSuffix="_matk.py"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	sed -i "s/Paper2_ParamSweep_4percent/Paper2_ParamSweep_300m/g" $runName$Suffix$matkSuffix
done
