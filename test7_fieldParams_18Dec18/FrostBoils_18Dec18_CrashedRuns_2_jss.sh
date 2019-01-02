#!/bin/bash

#PBS -q batch
#PBS -M oconnormt@ornl.gov
#PBS -A ccsi
#PBS -W group_list=cades-ccsi
#PBS -m be a
#PBS -N FrostBoils_18Dec18_matk
#PBS -l nodes=1:ppn=32 ### requested number of processors
#PBS -l walltime=48:00:00

cd $PBS_O_WORKDIR
module unload matk
module unload ats/0.88/Debug
module unload ats/0.88/Release

module load matk
module load ats/0.88/Release

myApp="python FrostBoils_18Dec18_CrashedRuns_2_matk.py"

echo $myApp > out.log
$myApp >>out.log
