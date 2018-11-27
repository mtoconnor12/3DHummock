#!/bin/bash

#PBS -q batch
#PBS -M oconnormt@ornl.gov
#PBS -A ccsi
#PBS -W group_list=cades-ccsi
#PBS -m be a
#PBS -N matk_ats
#PBS -l nodes=1:ppn=32 ### requested number of processors
#PBS -l walltime=24:00:00

cd /lustre/or-hydra/cades-ccsi/oconnormt/repo/3DHummock-try3/test7_matk/CenturySim_Debug.18_Debug
module unload matk
module unload ats/0.88/Debug
module unload ats/0.88/Release

module load matk
module load ats/0.88/Release

myApp="ats --xml_file=run.xml"

echo $myApp > out.log
$myApp >>out.log
