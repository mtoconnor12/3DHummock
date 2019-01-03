#!/usr/bin/env bash


Suffix="_18Dec18"
matkSuffix="_matk.py"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	sed -i "s/hillslope-fieldParams_18Dec18/Paper2_ParamSweep_4percent/g" $runName$Suffix$matkSuffix
done
