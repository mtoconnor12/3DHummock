#!/bin/bash

#PBS -q batch
#PBS -M oconnormt@ornl.gov
#PBS -A ccsi
#PBS -W group_list=cades-ccsi
#PBS -m be a
#PBS -N matk_ats
#PBS -l nodes=1:ppn=32 ### requested number of processors
#PBS -l walltime=36:00:00

cd $PBS_O_WORKDIR
module unload matk
module unload ats/0.88/Debug
module unload ats/0.88/Release

module load matk
module load ats/0.88/Release

myApp="python CenturySim_Debug_27Nov18_matk_ats.py"

echo $myApp > out.log
$myApp >>out.log
