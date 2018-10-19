#!/usr/bin/env bash

#PBS -q batch
#PBS -M oconnormt@ornl.gov  ### my ornl email
#PBS -A ccsi ### project
#PBS -W group_list=cades-ccsi ### don’t change
#PBS -m be a   ### email notifications at the beginning, ending, and abort
#PBS -N oconnorTest7 ### name of the job, same as the input file (doesn’t have to be)
###PBS -j oe
#PBS -l nodes=1:ppn=32 ### requested number of processors 
#PBS -l walltime=48:00:00 ### wall time (max time = 48h)

cd $PBS_O_WORKDIR

myApp="python matk_ats.py"

echo $myApp > out.log
$myApp >>out.log