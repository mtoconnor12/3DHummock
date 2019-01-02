#!/bin/bash

suffix="_18Dec18_CrashedRuns_2_jss.sh"

for runName in TussockTundraHi TussockTundraLo WaterTrack WoodyShrubsHillslope SedgeHi WoodyShrubsRiparianHi SedgeLo FrostBoils
do
	set -x #echo on
	qsub $runName$suffix
	set +x
done
