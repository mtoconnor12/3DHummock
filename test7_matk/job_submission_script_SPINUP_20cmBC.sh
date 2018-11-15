#!/bin/bash

#PBS -q batch
#PBS -M oconnormt@ornl.gov
#PBS -A ccsi
#PBS -W group_list=cades-ccsi
#PBS -m be a
#PBS -N matk_ats
#PBS -l nodes=1:ppn=32 ### requested number of processors
#PBS -l walltime=36:00:00

cd /lustre/or-hydra/cades-ccsi/oconnormt/repo/3DHummock-try3/test7_matk
module unload matk
module unload ats/0.88/Debug
module unload ats/0.88/Release

module load matk
module load ats/0.88/Release

myApp="python matk_ats_SPINUP_20cmBC.py"

echo $myApp > out.log
$myApp >>out.log
