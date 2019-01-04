#!/bin/bash

#PBS -q batch
#PBS -M oconnormt@ornl.gov
#PBS -A ccsi
#PBS -W group_list=cades-ccsi
#PBS -m be a
#PBS -N 3DHummock_03Jan18
#PBS -l nodes=1:ppn=32 ### requested number of processors
#PBS -l walltime=48:00:00

cd $PBS_O_WORKDIR
module unload matk
module unload ats/0.88/Debug
module unload ats/0.88/Release

module load ats/0.88/Release

myApp="mpirun -np 32 ats --xml_file=../test7_Paper3_NoCheckpoints_NoVerbosity_Default.xml"

echo $myApp > out.log
$myApp >>out.log
